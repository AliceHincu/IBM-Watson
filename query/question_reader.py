import re


class QuestionReader:
    def __init__(self, questions_file='questions.txt'):
        self.questions_file = questions_file

    def read_questions(self):
        pattern = re.compile(r"[.,:;!?-]")  # Define the pattern to remove punctuation.
        questions = []
        with open(self.questions_file, 'r', encoding='utf-8') as file:
            content = file.read().strip()
            question_blocks = content.split('\n\n')
            for block in question_blocks:
                lines = block.split('\n')
                if len(lines) >= 3:  # Ensure there are at least category, clue, and answer lines.
                    category = re.sub(pattern, "", lines[0].strip())
                    clue = re.sub(pattern, "", lines[1].strip())
                    answer = lines[2].strip()
                    questions.append((category, clue, answer))
        return questions
