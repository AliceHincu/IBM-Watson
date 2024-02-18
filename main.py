import nltk
from performance.mrr import MRRCalculator
from query.query_runner import QueryRunner
from query.question_reader import QuestionReader

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')


def run_default_questions(questions_file='questions.txt', index_path='indexdir7'):
    qr = QueryRunner(index_path)
    mrr_calc = MRRCalculator()
    qr_reader = QuestionReader(questions_file)

    questions = qr_reader.read_questions()
    ranks = []
    for category, clue, answer in questions:
        rank = qr.run_single_query(category, clue, answer)
        ranks.append(rank)

    mrr = mrr_calc.compute_mrr([rank for rank in ranks if rank])
    print(f"The MRR is: {mrr:.3f}")
    print(f"The correct number of top positions: {ranks.count(1)}/{len(ranks)}")


if __name__ == '__main__':
    # 1. create index
    # create_index()

    # Call the function to print out the content of the first few indexed documents
    # verify_index_content()

    # 2. run default queries
    run_default_questions()
