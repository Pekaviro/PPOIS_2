from typing import Any, Dict, List, Tuple

from .exam import Exam



class PreviousExamAttempt:
    def __init__(self, exam: 'Exam', answers: List[str]) -> None:
        self.exam: 'Exam' = exam
        self.answers: List[str] = answers

    def to_dict(self) -> Dict[str, Any]:
        return {
            "exam": self.exam.to_dict(),
            "answers": self.answers
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'PreviousExamAttempt':
        try:
            if not data or 'exam' not in data or 'answers' not in data:
                raise ValueError("Некорректные данные для создания PreviousExamAttempt.")

            exam = Exam.from_dict(data['exam'])
            answers = data['answers']

            if not isinstance(answers, list):
                raise ValueError("Ответы должны быть представлены в виде списка.")

            return cls(exam, answers)
        except Exception as e:
            print(f"Ошибка при создании объекта PreviousExamAttempt: {e}")
            raise

    def calculate_score(self) -> int:
        try:
            if not self.exam.questions or not self.answers:
                return 0

            correct_answers = 0
            for (_, _, correct_answer), student_answer in zip(self.exam.questions, self.answers):
                if student_answer == correct_answer:
                    correct_answers += 1

            return correct_answers
        except Exception as e:
            print(f"Ошибка при подсчёте правильных ответов: {e}")
            return 0

    def display_results(self) -> None:
        try:
            if not self.exam.questions or not self.answers:
                print("Данные экзамена или ответы отсутствуют.")
                return

            print(f"Результаты попытки сдачи экзамена по предмету '{self.exam.subject}':")
            for i, ((topic, question, correct_answer), student_answer) in enumerate(zip(self.exam.questions, self.answers), 1):
                print(f"\nВопрос {i}: {question}")
                print(f"Тема: {topic}")
                print(f"Ваш ответ: {student_answer}")
                print(f"Правильный ответ: {correct_answer}")
                print("-" * 20)

            score = self.calculate_score()
            print(f"\nИтого: {score} из {len(self.exam.questions)} правильных ответов.")
        except Exception as e:
            print(f"Ошибка при отображении результатов: {e}")
