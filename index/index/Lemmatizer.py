import nltk
from nltk import WordNetLemmatizer
from whoosh.analysis import Token, Filter
import index.utils.utils as shared

nltk.download('wordnet')

class Lemmatizer(Filter):
    """
    This is a custom Lemmatizer class that extends Whoosh's Filter to provide lemmatization capabilities for tokens during
    indexing or querying. It initializes with a WordNet lemmatizer and processes each token, applying lemmatization
    to the token's text. The class adapts its behavior based on whether it's used for querying or indexing, preserving
    necessary token attributes like pos (part of speech) for indexing. This ensures that tokens are reduced to their
    base or dictionary forms, improving the consistency and relevancy of search results by aligning varied word forms.
    """

    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()

    def __call__(self, tokens):
        for t in tokens:
            lemmatized_text = self.lemmatizer.lemmatize(t.text)
            if shared.choice == "query":
                yield Token(text=lemmatized_text, boost=t.boost, stopped=t.stopped, removestops=t.removestops, mode=t.mode)
            else:
                yield Token(text=lemmatized_text, pos=t.pos, boost=t.boost, stopped=t.stopped, removestops=t.removestops, mode=t.mode)