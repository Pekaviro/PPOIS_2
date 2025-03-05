import unittest
import json
import os
from pathlib import Path
from unittest.mock import patch, MagicMock
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from entities.exam import Exam

class TestExam(unittest.TestCase):

    def setUp(self):
        self.test_file = Path("test_storage/test_exams.json")
        Exam.STORAGE_FILE = self.test_file
        self.exam = Exam(subject="Математика")
        self.exam.questions = [
            ("Линейные уравнения", "Найдите корень уравнения 2x=4", "2"),
            ("Производная простой функции", "Какова производная от x^2?", "2x")
        ]


    def test_set_info(self):
        # Очищаем данные экзаменов
        Exam.STORAGE_FILE.unlink(missing_ok=True)

        with patch('builtins.input', side_effect=[
            "Математика",     # Введите название предмета
            "Линейные уравнения",         # Введите тему
            "Найдите корень уравнения 2x=4",   # Введите вопрос
            "2",               # Введите ответ
            "да",              # Хотите добавить ещё один вопрос?
            "Производная простой функции",        # Введите тему
            "Какова производная от x^2?",   # Введите вопрос
            "2x",              # Введите ответ
            "нет"              # Хотите добавить ещё один вопрос?
        ]):
            with patch('builtins.print') as mock_print:
                self.exam.set_info()

                # Выведем фактические вызовы print
                actual_print_calls = [call[0][0] for call in mock_print.call_args_list]
                for call in actual_print_calls:
                    print(f"print call: {call}")

                # Проверяем, что предмет установлен правильно
                self.assertEqual(self.exam.subject, "Математика")

                # Проверяем, что вопросы добавлены правильно
                self.assertEqual(len(self.exam.questions), 2)
                self.assertEqual(self.exam.questions[0], ("Линейные уравнения", "Найдите корень уравнения 2x=4", "2"))
                self.assertEqual(self.exam.questions[1], ("Производная простой функции", "Какова производная от x^2?", "2x"))

                # Проверяем вывод сообщений
                expected_calls = [
                    "\nВведите данные для нового вопроса (тема, вопрос, ответ).",
                    "\nДанные экзамена успешно сохранены!"
                ]
                for expected_call in expected_calls:
                    self.assertIn(expected_call, actual_print_calls, f"Expected call '{expected_call}' not found in actual calls: {actual_print_calls}")

    def test_display_exams(self):
        with patch('builtins.print') as mock_print:
            self.exam.save()
            Exam.display_exams()
            mock_print.assert_any_call("\nСписок экзаменов:")
            mock_print.assert_any_call("- Математика")

    def test_load(self):
        self.exam.save()
        loaded_exam = Exam.load("Математика")
        self.assertIsNotNone(loaded_exam)
        self.assertEqual(loaded_exam.subject, "Математика")
        self.assertEqual(loaded_exam.questions, [
            ("Линейные уравнения", "Найдите корень уравнения 2x=4", "2"),
            ("Производная простой функции", "Какова производная от x^2?", "2x")
        ])

    def test_load_not_found(self):
        with patch('builtins.print') as mock_print:
            loaded_exam = Exam.load("Physics")
            self.assertIsNone(loaded_exam)
            mock_print.assert_any_call("Экзамен по предмету 'Physics' не найден.")

    def test_load_all(self):
        self.exam.save()
        exams = Exam.load_all()
        self.assertIn("Математика", exams)
        self.assertEqual(exams["Математика"]["subject"], "Математика")
        self.assertEqual(
            [tuple(q) for q in exams["Математика"]["questions"]],
            [("Линейные уравнения", "Найдите корень уравнения 2x=4", "2"), ("Производная простой функции", "Какова производная от x^2?", "2x")]
        )

    def test_save(self):
        with patch('builtins.print') as mock_print:
            self.exam.save()
            mock_print.assert_any_call("Экзамен по предмету 'Математика' успешно сохранён.")
            exams = Exam.load_all()
            self.assertIn("Математика", exams)

    def test_delete(self):
        self.exam.save()
        with patch('builtins.print') as mock_print:
            self.exam.delete()
            mock_print.assert_any_call("Экзамен по предмету 'Математика' удалён из системы.")
            exams = Exam.load_all()
            self.assertNotIn("Математика", exams)

    def test_to_dict(self):
        exam_dict = self.exam.to_dict()
        self.assertEqual(exam_dict["subject"], "Математика")
        self.assertEqual(exam_dict["questions"], [
            ("Линейные уравнения", "Найдите корень уравнения 2x=4", "2"),
            ("Производная простой функции", "Какова производная от x^2?", "2x")
        ])

    def test_from_dict(self):
        exam_dict = {
            "subject": "Математика",
            "questions": [
                ("Линейные уравнения", "Найдите корень уравнения 2x=4", "2"),
                ("Производная простой функции", "Какова производная от x^2?", "2x")
            ]
        }
        loaded_exam = Exam.from_dict(exam_dict)
        self.assertEqual(loaded_exam.subject, "Математика")
        self.assertEqual(loaded_exam.questions, [
            ("Линейные уравнения", "Найдите корень уравнения 2x=4", "2"),
            ("Производная простой функции", "Какова производная от x^2?", "2x")
        ])

if __name__ == '__main__':
    unittest.main()
