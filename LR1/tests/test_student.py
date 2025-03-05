import unittest
import json
import os
from pathlib import Path
import sys
from unittest.mock import MagicMock, patch

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from entities.additional_classes import AdditionalClasses
from entities.student import Student
from entities.exam import Exam
from entities.previous_exam_attempt import PreviousExamAttempt
from entities.educational_materials import EducationalMaterial



class TestStudent(unittest.TestCase):

    def setUp(self):
        self.test_file = Path("test_storage/test_students.json")
        Student.STORAGE_FILE = self.test_file
        self.student = Student(id="12345")
        self.student.last_name = "Иванов"
        self.student.first_name = "Иван"
        self.exam = Exam(subject="Математика")
        self.exam.questions = [
            ("Линейные уравнения", "Найдите корень уравнения 2x=4", "2"),
            ("Производная простой функции", "Какова производная от x^2?", "2x")
        ]
        self.student.exam_result = PreviousExamAttempt(
            exam=self.exam,
            answers=["2", "2x"]
        )
        self.student.materials = [
            EducationalMaterial(topic="Линейные уравнения", title="Введение в алгебру", author="John Doe"),
            EducationalMaterial(topic="Производная простой функции", title="Интегралы и производные", author="Jane Doe")
        ]
        self.student.unexplored_topics = {"Линейные уравнения", "Производная простой функции"}

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_set_info(self):
        with unittest.mock.patch('builtins.input', side_effect=["12345", "Иванов", "Иван"]):
            self.student.set_info()
            self.assertEqual(self.student.id, "12345")
            self.assertEqual(self.student.last_name, "Иванов")
            self.assertEqual(self.student.first_name, "Иван")

    def test_analyze_errors(self):
        errors = self.student.analyze_errors()
        self.assertEqual(len(errors), 0)  # No errors

        self.student.exam_result.answers = ["1", "2"]
        errors = self.student.analyze_errors()
        self.assertEqual(len(errors), 2)  # All answers incorrect

    def test_display_errors(self):
        with unittest.mock.patch('builtins.print') as mock_print:
            self.student.display_errors()
            mock_print.assert_called_with(f"{self.student.last_name} {self.student.first_name} не допустил(а) ошибок на экзамене по Математика.")

        self.student.exam_result.answers = ["1", "2"]
        with unittest.mock.patch('builtins.print') as mock_print:
            self.student.display_errors()
            mock_print.assert_any_call(f"Ошибки {self.student.last_name} {self.student.first_name} на экзамене по Математика:")

    def test_study_materials(self):
        self.student.materials = []
        with patch('builtins.print') as mocked_print:
            self.student.study_materials()
            mocked_print.assert_called_with("Нет рекомендованной литературы для изучения. Советуем посетить консультацию.")

    def test_re_passing_the_exam(self):
        with unittest.mock.patch('builtins.input', side_effect=["2", "2x"]):
            with unittest.mock.patch('builtins.print') as mock_print:
                self.student.re_passing_the_exam()
                mock_print.assert_any_call(f"{self.student.last_name} {self.student.first_name} сдал экзамен по Математика.")

        with unittest.mock.patch('builtins.input', side_effect=["1", "2"]):
            with unittest.mock.patch('builtins.print') as mock_print:
                self.student.re_passing_the_exam()
                mock_print.assert_any_call(f"{self.student.last_name} {self.student.first_name} не сдал экзамен по Математика.")

    def test_save_and_load(self):
        self.student.save()
        loaded_student = Student.load("12345")
        self.assertIsNotNone(loaded_student)
        self.assertEqual(loaded_student.id, "12345")
        self.assertEqual(loaded_student.last_name, "Иванов")
        self.assertEqual(loaded_student.first_name, "Иван")

    def test_delete(self):
        self.student.save()
        self.student.delete()
        loaded_student = Student.load("12345")
        self.assertIsNone(loaded_student)

    def test_id_exist(self):
        self.student.save()
        self.assertTrue(Student.id_exist("12345"))
        self.assertFalse(Student.id_exist("54321"))

    def test_to_dict(self):
        student_dict = self.student.to_dict()
        self.assertEqual(student_dict['id'], "12345")
        self.assertEqual(student_dict['last_name'], "Иванов")
        self.assertEqual(student_dict['first_name'], "Иван")

    def test_from_dict(self):
        student_dict = {
            "id": "12345",
            "last_name": "Иванов",
            "first_name": "Иван",
            "exam_result": self.student.exam_result.to_dict(),
            "materials": [material.to_dict() for material in self.student.materials],
            "unexplored_topics": list(self.student.unexplored_topics)
        }
        loaded_student = Student.from_dict(student_dict)
        self.assertEqual(loaded_student.id, "12345")
        self.assertEqual(loaded_student.last_name, "Иванов")
        self.assertEqual(loaded_student.first_name, "Иван")

    def test_display_unexplored_topics(self):
        with unittest.mock.patch('builtins.print') as mock_print:
            self.student.display_unexplored_topics()
            mock_print.assert_any_call(f"\nСписок неизученных тем для {self.student.last_name} {self.student.first_name}:")
            mock_print.assert_any_call("- Линейные уравнения")
            mock_print.assert_any_call("- Производная простой функции")

if __name__ == '__main__':
    unittest.main()
