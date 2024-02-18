class WikipediaPage:
    def __init__(self, title="", categories=None, content=""):
        self.title = title
        self.categories = categories if categories else []
        self.content = content
