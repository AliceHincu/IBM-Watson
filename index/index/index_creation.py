import os

from whoosh.analysis import StemmingAnalyzer
from whoosh.fields import Schema, TEXT, KEYWORD
from whoosh.index import create_in

from index.utils.utils import get_files_from_directory
from index.wikipedia_page.WikipediaPageParser import WikiPageParser

wiki_directory_path = 'wikipedia_pages'
index_directory_path = 'indexdir7'


def create_index(wikipedia_directory=wiki_directory_path,index_path=index_directory_path):
    # Define the schema for your index
    schema = Schema(
        title=TEXT(stored=True, analyzer=StemmingAnalyzer()),
        content=TEXT(analyzer=StemmingAnalyzer()),
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

    for file in files:
        parser = WikiPageParser(file)
        result = parser.parse()

        page_set.update(result['page_set'])
        redirect_page_titles.update(result['redirect_page_titles'])

    print("Finished parsing files")

    for wiki_page in page_set:
        redirected_pages = redirect_page_titles.get(wiki_page.title, [])
        doc = {
            "title": wiki_page.title,
            "content": wiki_page.content,
            "category": ",".join(wiki_page.categories)
        }

        writer.add_document(**doc)

        for title in redirected_pages:
            redirect_doc = {
                "title": title,
                "content": "",
                "category": ",".join(wiki_page.categories)  # Assuming redirects share categories
            }
            writer.add_document(**redirect_doc)

    print("Saving index to file ...")

    writer.commit()
    print("Finished all")