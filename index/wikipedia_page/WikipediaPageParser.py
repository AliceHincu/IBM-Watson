# import re
#
# from index.wikipedia_page.WikipediaPage import WikipediaPage
#
#
# class WikiPageParser:
#     TITLE_PATTERN = r"^\[\[(.*?)]]$"
#     CATEGORY_PREFIX = "CATEGORIES:"
#     REDIRECT_PREFIX = "#REDIRECT "
#
#     def __init__(self, file_path):
#         self.file_path = file_path
#         self.page_set = set()
#         self.redirect_page_titles = {}
#         self.page_content = ""
#         self.page = WikipediaPage()
#         self.was_redirect = False
#
#     def parse(self):
#         with open(self.file_path, 'r', encoding='utf-8') as file:
#             for line in file:
#                 self.process_line(line.strip())
#
#         # After processing all lines, check if the last page needs to be added
#         self.finalize_current_page()
#
#         return {
#             "page_set": self.page_set,
#             "redirect_page_titles": self.redirect_page_titles
#         }
#
#     def process_line(self, line):
#         if not line:  # Skip blank lines
#             return
#
#         if self.is_title(line):
#             self.finalize_current_page()
#             self.was_redirect = False
#             self.page = WikipediaPage()
#             self.page.title = self.retrieve_title(line)
#         elif self.is_category_line(line):
#             self.page.categories = self.tokenize_category_line(line)
#         elif self.is_redirect_line(line):
#             redirect_page = self.get_redirect_page_title(line)
#             self.redirect_page_titles.setdefault(redirect_page, []).append(self.page.title)
#             self.was_redirect = True
#         else:
#             self.page_content += line
#
#     def finalize_current_page(self):
#         if self.page.title and not self.was_redirect:
#             self.page.content = self.page_content
#             self.page_set.add(self.page)
#             self.page_content = ""
#
#     def is_title(self, input):
#         return re.match(self.TITLE_PATTERN, input) is not None
#
#     def retrieve_title(self, input):
#         return input.strip("[]")
#
#     def is_category_line(self, input):
#         return input.startswith(self.CATEGORY_PREFIX)
#
#     def tokenize_category_line(self, input):
#         return input[len(self.CATEGORY_PREFIX):].split(", ")
#
#     def is_redirect_line(self, input):
#         return input.startswith(self.REDIRECT_PREFIX)
#
#     def get_redirect_page_title(self, input):
#         return input[len(self.REDIRECT_PREFIX):]
import re

from index.wikipedia_page.WikipediaPage import WikipediaPage


class WikiPageParser:
    TITLE_PATTERN = re.compile(r'^\[\[(.*?)]]$')
    CATEGORY_PATTERN = re.compile(r'^CATEGORIES:(.*)')
    REDIRECT_PATTERN = re.compile(r'(?i)^#REDIRECT (.*)')

    def __init__(self, file_path):
        self.file_path = file_path
        self.page_set = set()
        self.redirect_page_titles = {}

    def parse(self):
        with open(self.file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        pages = content.split("\n\n\n")
        for page in pages:
            self.process_page(page)

        return {
            "page_set": self.page_set,
            "redirect_page_titles": self.redirect_page_titles
        }

    def process_page(self, page_content):
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
                page.categories = category_match.group(1).split(", ")
            else:
                page.content += line

        if page.title and page.title not in self.redirect_page_titles:
            self.page_set.add(page)

    # def finalize_current_page(self):
    #     if self.page.title and not self.was_redirect:
    #         self.page.content = self.page_content
    #         self.page_set.add(self.page)
    #         self.page_content = ""
    #
    # def is_title(self, input):
    #     return re.match(self.TITLE_PATTERN, input) is not None
    #
    # def retrieve_title(self, input):
    #     return input.strip("[]")
    #
    # def is_category_line(self, input):
    #     return input.startswith(self.CATEGORY_PREFIX)
    #
    # def tokenize_category_line(self, input):
    #     return input[len(self.CATEGORY_PREFIX):].split(", ")
    #
    # def is_redirect_line(self, input):
    #     return input.startswith(self.REDIRECT_PREFIX)
    #
    # def get_redirect_page_title(self, input):
    #     return input[len(self.REDIRECT_PREFIX):]
