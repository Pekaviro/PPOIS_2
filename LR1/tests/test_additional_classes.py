import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from unittest.mock import patch, MagicMock
from entities.educational_materials import EducationalMaterial
from entities.student import Student
from entities.additional_classes import AdditionalClasses

class TestAdditionalClasses(unittest.TestCase):

    def setUp(self):
        self.student = Student(id="12345")
        self.student.last_name = "Иванов"
        self.student.first_name = "Иван"
        self.additional_classes = AdditionalClasses(self.student, "Линейные уравнения")

    @patch('entities.educational_materials.EducationalMaterial.load_all', return_value={
        "Линейные уравнения": {"subject": "Математика", "topic": "Линейные уравнения", "title": "Введение в алгебру", "author": "John Doe"}
    })
    @patch('entities.student.Student.save')
    def test_recommend_literature(self, mock_save, mock_load_all):
        with patch('builtins.print') as mock_print:
            self.additional_classes.recommend_literature()
            self.assertTrue(any("Рекомендованная литература:" in call[0][0] for call in mock_print.call_args_list))
            self.assertTrue(any("- Введение в алгебру (автор: John Doe)" in call[0][0] for call in mock_print.call_args_list))
            self.assertEqual(len(self.student.materials), 1)
            mock_save.assert_called_once()

    @patch('entities.educational_materials.EducationalMaterial.load_all', return_value={})
    def test_recommend_literature_not_found(self, mock_load_all):
        with patch('builtins.print') as mock_print:
            self.additional_classes.recommend_literature()
            self.assertTrue(any("Литература по данной теме не найдена." in call[0][0] for call in mock_print.call_args_list))
            self.assertIsNone(self.student.materials)

    @patch('entities.educational_materials.EducationalMaterial.load_all', side_effect=FileNotFoundError)
    def test_recommend_literature_file_not_found(self, mock_load_all):
        with patch('builtins.print') as mock_print:
            self.additional_classes.recommend_literature()
            self.assertTrue(any("Ошибка: файл с учебными материалами не найден." in call[0][0] for call in mock_print.call_args_list))
            self.assertIsNone(self.student.materials)

    def test_conduct_consultation(self):
        with patch('entities.additional_classes.AdditionalClasses.recommend_literature', side_effect=Exception("Test Exception")):
            with patch('builtins.print') as mock_print:
                self.additional_classes.conduct_consultation()
                self.assertTrue(any("Произошла ошибка во время консультации: Test Exception" in call[0][0] for call in mock_print.call_args_list))
                self.assertTrue(any("Консультация завершена." in call[0][0] for call in mock_print.call_args_list))

if __name__ == '__main__':
    unittest.main()
