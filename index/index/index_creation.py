import os

from whoosh.analysis import RegexTokenizer, LowercaseFilter, StopFilter, CharsetFilter
from whoosh.fields import Schema, TEXT, KEYWORD
from whoosh.index import create_in
from whoosh.support.charset import accent_map

from index.index.Lemmatizer import Lemmatizer
from index.utils.utils import get_files_from_directory
from index.wikipedia_page.WikipediaPageParser import WikiPageParser
from nltk.corpus import stopwords

wiki_directory_path = 'wikipedia_pages'
index_directory_path = 'indexdir8'
ENGLISH_STOP_WORDS = set(stopwords.words('english'))
custom_analyzer = (RegexTokenizer() | LowercaseFilter() | StopFilter(stoplist=ENGLISH_STOP_WORDS) | Lemmatizer() |
                   CharsetFilter(accent_map))


def create_index(wikipedia_directory=wiki_directory_path,index_path=index_directory_path):
    """
    Creates a search index from Wikipedia pages.

    This function defines the schema for the index with title, content, and category fields.
    It then reads through all files in the given directory, parses each file to extract page
    data, and adds this data to the search index.


    The function begins by clearing any existing index in the specified path and then creates
    a new index. For each Wikipedia page, it extracts the title, content, and categories and
    adds a document to the index. If a page is a redirect, it adds an entry for the redirect
    target as well.

    Args:
        wikipedia_directory (str): The directory path where Wikipedia pages are stored.
        index_path (str): The directory path where the search index will be stored.
    """
    schema = Schema(
        title=TEXT(stored=True, analyzer=custom_analyzer),
        content=TEXT(analyzer=custom_analyzer),
        category=KEYWORD(commas=True, scorable=True, stored=True)
    )

    # Delete existing index files to start fresh
    if os.path.exists(index_path):
        for filename in os.listdir(index_path):
            os.remove(os.path.join(index_path, filename))
    else:
        os.makedirs(index_path)

    # Create a new index
    ix = create_in(index_path, schema)
    writer = ix.writer()

    # get the files with the wikipedia pages
    files = get_files_from_directory(wikipedia_directory)

    page_set, redirect_page_titles = set(), {}

    print("Started parsing files")
    for file in files:
        parser = WikiPageParser(file)
        result = parser.parse()

        page_set.update(result.get_processed_wikipedia_pages())
        redirect_page_titles.update(result.get_redirect_page_titles())
    print("Finished parsing files")

    print("Saving wikipedia pages to index")
    for wiki_page in page_set:
        redirected_pages = redirect_page_titles.get(wiki_page.title, [])
        writer.add_document(title=wiki_page.title, content=wiki_page.content, category=wiki_page.categories)

        for title in redirected_pages:
            writer.add_document(title=title, content="", category=wiki_page.categories)
    print("Finished saving pages to index")

    print("Saving index...")
    writer.commit()
    print("Finished all")