from whoosh.analysis import StemmingAnalyzer
from whoosh.index import open_dir
from whoosh.qparser import MultifieldParser, OrGroup

from whoosh.lang import porter
from nltk.corpus import wordnet as wn

from index.index.index_creation import custom_analyzer


class QueryRunner:
    def __init__(self, index_path='indexdir8'):
        self.index_path = index_path

    def preprocess_with_analyzer(self, text, analyzer):
        """
        Preprocesses the given text using the specified Whoosh analyzer.

        Args:
            text (str): The text to preprocess.
            analyzer (Analyzer): The Whoosh analyzer to use for preprocessing.

        Returns:
            str: The preprocessed text.
        """
        tokens = [token.text for token in analyzer(text)]
        return " ".join(tokens)

    def run_single_query(self, category, clue, answer):
        """
        Executes a search query against the index using a given category and clue, comparing the results against a specified answer.

        This method preprocesses the category and clue using a StemmingAnalyzer to ensure that the search terms match the indexed content more effectively. It constructs a query that searches for documents matching either the preprocessed clue or category. The search is performed within the "content" and "category" fields of the index.

        Args:
            category (str): The category related to the clue, which may contain additional descriptors within parentheses that are stripped during preprocessing.
            clue (str): The clue or question that needs to be answered.
            answer (str): The expected answer, which can include multiple correct responses separated by "|".

        Returns:
            int: The rank (1-based) of the first document in the search results that matches any of the expected answers
            , or 0 if none of the documents match.

        Prints the clue, category, expected answer, and the title of the first matching document found in the index (if
        any). If no document matches the expected answer, prints 'Not found'.
        """
        directory = open_dir(self.index_path)
        searcher = directory.searcher()

        analyzer = custom_analyzer
        preprocessed_clue = self.preprocess_with_analyzer(clue, analyzer)
        preprocessed_category = category.split("(")[0].strip().replace('"', '')

        query_string = f"({preprocessed_clue}) OR ({preprocessed_category})"

        parser = MultifieldParser(["content", "category"], schema=directory.schema, group=OrGroup.factory(0.9))
        query = parser.parse(query_string)

        results = searcher.search(query, limit=10)

        correct_answers = set(answer.split("|"))
        result_rank = 0

        for i, hit in enumerate(results):
            if hit['title'] in correct_answers:
                result_rank = i + 1
                break

        print(
            f"\n\nClue: {clue}\nCategory: {category}\nExpected answer: {answer}\nIndex answer: {hit['title'] if result_rank else 'Not found'}")
        searcher.close()
        return result_rank

    def get_synonyms(self, word):
        """
        Retrieves synonyms for a given word using NLTK's WordNet.

        Args:
            word (str): The word for which to find synonyms.

        Returns:
            set: A set of synonyms for the word.
        """
        synonyms = []
        for syn in wn.synsets(word):
            for lemma in syn.lemmas():
                synonym = lemma.name().replace('_', ' ')
                synonyms.append(porter.stem(synonym))
        return synonyms[:2]

    def preprocess_with_analyzer_and_synonyms(self,text, analyzer):
        """
        Preprocesses text with an analyzer and expands it with synonyms.

        Args:
            text (str): The text to preprocess.
            analyzer (Analyzer): The Whoosh analyzer for initial preprocessing.

        Returns:
            str: A string with the original processed terms and their synonyms.
        """
        processed_tokens = [token.text for token in analyzer(text)]
        expanded_terms = []
        for token in processed_tokens:
            synonyms = self.get_synonyms(token)
            expanded_terms.append(f"({' OR '.join([token] + list(synonyms))})")
        return ' OR '.join(expanded_terms)

    def run_single_query_with_synonyms(self, category, clue, answer):
        directory = open_dir(self.index_path)
        searcher = directory.searcher()
        analyzer = StemmingAnalyzer()

        # Preprocess clue and category with synonyms
        preprocessed_clue = self.preprocess_with_analyzer_and_synonyms(clue, analyzer)
        preprocessed_category = self.preprocess_with_analyzer_and_synonyms(category.split("(")[0].strip(), analyzer)

        # Construct the query string
        query_string = f"({preprocessed_clue}) OR ({preprocessed_category})"
        parser = MultifieldParser(["content", "category"], schema=directory.schema, group=OrGroup.factory(0.9))
        query = parser.parse(query_string)

        results = searcher.search(query, limit=10)
        print(f"Found {len(results)} hits.")

        # Evaluate the results against the correct answers
        correct_answers = set(answer.split("|"))
        result_rank = 0
        for i, hit in enumerate(results):
            if hit['title'] in correct_answers:
                result_rank = i + 1
                break

        print(
            f"Clue: {clue}\nCategory: {category}\nExpected answer: {answer}\nIndex answer: {hit['title'] if result_rank else 'Not found'}")
        searcher.close()
        return result_rank
