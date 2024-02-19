import nltk

from index.index.index_creation import create_index
from performance.mrr import MRRCalculator
from query.query_runner import QueryRunner
from query.question_reader import QuestionReader
import index.utils.utils as shared

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')


def run_default_questions(questions_file='questions.txt', index_path='indexdir8'):
    qr = QueryRunner(index_path)
    mrr_calc = MRRCalculator()
    qr_reader = QuestionReader(questions_file)

    questions = qr_reader.read_questions()
    ranks = []
    answer_ranks = [0 for _ in range(11)]
    for category, clue, answer in questions:
        rank = qr.run_single_query(category, clue, answer)
        answer_ranks[rank - 1] += 1
        ranks.append(rank)

    mrr = mrr_calc.compute_mrr([rank for rank in ranks if rank])
    print(f"The MRR is: {mrr:.3f}")
    print(f"The correct number of top positions: {ranks.count(1)}/{len(ranks)}")
    print(f"The top 10 answer ranks: {answer_ranks}")


def show_menu():
    print("Menu:")
    print("1. Create Index")
    print("2. Run Default Questions")
    print("0. Exit")


if __name__ == '__main__':
    running = True
    while running:
        show_menu()
        option = input(">> ")
        if option == '1':
            shared.choice = "index"
            create_index()
        elif option == '2':
            shared.choice = "query"
            run_default_questions()
        elif option == '0':
            running = False
