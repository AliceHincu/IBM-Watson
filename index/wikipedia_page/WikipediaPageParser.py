import re

from index.utils.utils import preprocess_file_content
from index.wikipedia_page.ParseResult import ParseResult
from index.wikipedia_page.WikipediaPage import WikipediaPage


class WikiPageParser:
    """
    A parser class to extract information about wiki pages from a text file.

    Attributes:
        file_path (str): The path to the file containing wiki page contents.
        processed_wikipedia_pages (set): A set to store processed WikipediaPage objects.
        redirect_page_titles (dict): A dictionary, mapping page titles to their redirect targets.
    """

    TITLE_PATTERN = re.compile(r'^\[\[(.*?)]]$')
    CATEGORY_PATTERN = re.compile(r'^CATEGORIES:(.*)')
    REDIRECT_PATTERN = re.compile(r'(?i)^#REDIRECT (.*)')

    def __init__(self, file_path):
        """
        Initializes the WikiPageParser with a file path.

        Args:
            file_path (str): The path to the file to parse.
        """
        self.file_path = file_path
        self.processed_wikipedia_pages = set()
        self.redirect_page_titles = {}

    def parse(self):
        """
        Reads the file at the initialized file path and processes its content into wiki pages.

        Returns:
            ParseResult: A dictionary with two keys, 'page_set' containing a set of WikiPage objects, and
            'redirect_page_titles' containing a mapping of titles to redirect targets.
        """
        with open(self.file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        cleaned_content = preprocess_file_content(content)
        pages = cleaned_content.split("\n\n\n")
        for page in pages:
            self.process_page(page)

        return ParseResult(self.processed_wikipedia_pages, self.redirect_page_titles)

    def process_page(self, page_content):
        """
        Processes the content of a single page. The page content is expected to be a string where different elements of
        the page such as the title, categories, and body are separated by newline characters. This method parses through
        each line to identify and set the title, categories, and body of a WikipediaPage object. It also identifies
        redirect lines and stores any found redirects in the redirect_page_titles dictionary.

        The page title is extracted using a regular expression that looks for the [[Title]] pattern.
        Categories are extracted from lines starting with 'CATEGORIES:'.
        Redirects are identified by lines starting with '#REDIRECT' and are case-insensitive.

        Any line that is not a title, category, or redirect is considered part of the page body.
        If the page title does not correspond to a redirect, the constructed WikipediaPage object is added to the
        processed_wikipedia_pages.

        Args:
            page_content (str): The content of a wiki page as a single string.
        """
        lines = page_content.split("\n")
        page = WikipediaPage()
        for line in lines:
            if not line:
                continue
            title_match = self.TITLE_PATTERN.match(line)
            if title_match:
                page.title = title_match.group(1)
            elif self.REDIRECT_PATTERN.match(line):
                redirect_match = self.REDIRECT_PATTERN.match(line)
                self.redirect_page_titles.setdefault(page.title, []).append(redirect_match.group(1))
            elif self.CATEGORY_PATTERN.match(line):
                category_match = self.CATEGORY_PATTERN.match(line)
                page.categories = category_match.group(1)
            else:
                page.content += line

        if page.title and page.title not in self.redirect_page_titles:
            self.processed_wikipedia_pages.add(page)
