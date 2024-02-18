class ParseResult:
    """
    A class to encapsulate the results of parsing Wikipedia page data.

    Attributes:
        processed_wikipedia_pages (set): A set of WikipediaPage objects that have been processed.
        redirect_page_titles (dict): A dictionary mapping titles of pages that are redirects to their target titles.
    """
    def __init__(self, processed_wikipedia_pages, redirect_page_titles):
        self.processed_wikipedia_pages = processed_wikipedia_pages
        self.redirect_page_titles = redirect_page_titles

    def get_processed_wikipedia_pages(self):
        return self.processed_wikipedia_pages

    def get_redirect_page_titles(self):
        return self.redirect_page_titles
