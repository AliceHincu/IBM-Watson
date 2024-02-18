class WikipediaPage:
    """
        A class representing a Wikipedia page.

        Attributes:
            title (str): The title of the Wikipedia page.
            categories (str): A list of categories associated with the page.
            content (str): The textual content of the page.

        The WikipediaPage class encapsulates all relevant information for a single Wikipedia page,
        including its title, associated categories, and the page's content.
        """
    def __init__(self, title="", categories="", content=""):
        self.title = title
        self.categories = categories
        self.content = content
