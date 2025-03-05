import os
import unittest
from unittest.mock import patch
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from entities.previous_exam_attempt import PreviousExamAttempt
from entities.exam import Exam

class TestPreviousExamAttempt(unittest.TestCase):

    def setUp(self):
        self.exam_data = {
            "subject": "Математика",
            "questions": [("Линейные уравнения", "Найдите корень уравнения 2x=4", "2"), ("Производная простой функции", "Какова производная от x^2?", "2x")]
        }
        self.exam = Exam.from_dict(self.exam_data)
        self.answers = ["2", "2x"]
        self.attempt = PreviousExamAttempt(self.exam, self.answers)

    def test_to_dict(self):
        expected = {
            "exam": self.exam_data,
            "answers": self.answers
        }
        self.assertEqual(self.attempt.to_dict(), expected)

    def test_from_dict(self):
        data = {
            "exam": self.exam_data,
            "answers": self.answers
        }
        attempt = PreviousExamAttempt.from_dict(data)
        self.assertEqual(attempt.exam.subject, self.exam.subject)
        self.assertEqual(attempt.answers, self.answers)

    def test_from_dict_invalid_data(self):
        with self.assertRaises(ValueError):
            PreviousExamAttempt.from_dict({})

        with self.assertRaises(ValueError):
            PreviousExamAttempt.from_dict({"exam": self.exam_data, "answers": "not a list"})

    def test_calculate_score(self):
        self.assertEqual(self.attempt.calculate_score(), 2)

        # Test with incorrect answers
        attempt_incorrect = PreviousExamAttempt(self.exam, ["1", "1"])
        self.assertEqual(attempt_incorrect.calculate_score(), 0)

    def test_display_results(self):
        expected_print_calls = [
            f"Результаты попытки сдачи экзамена по предмету 'Математика':",
            f"\nВопрос 1: Найдите корень уравнения 2x=4",
            "Тема: Линейные уравнения",
            "Ваш ответ: 2",
            "Правильный ответ: 2",
            "-" * 20,
            f"\nВопрос 2: Какова производная от x^2?",
            "Тема: Производная простой функции",
            "Ваш ответ: 2x",
            "Правильный ответ: 2x",
            "-" * 20,
            f"\nИтого: 2 из 2 правильных ответов."
        ]

        with patch('builtins.print') as mock_print:
            self.attempt.display_results()
            actual_print_calls = [call[0][0] for call in mock_print.call_args_list]
            for expected_call in expected_print_calls:
                self.assertIn(expected_call, actual_print_calls)

if __name__ == '__main__':
    unittest.main()
