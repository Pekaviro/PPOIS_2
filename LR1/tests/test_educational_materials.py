import unittest
import json
import os
from pathlib import Path
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from entities.educational_materials import EducationalMaterial



class TestEducationalMaterial(unittest.TestCase):

    def setUp(self):
        self.test_file = Path("test_storage/test_educational_materials.json")
        EducationalMaterial.STORAGE_FILE = self.test_file
        self.material = EducationalMaterial(topic="Линейные уравнения", title="Введение в алгебру", author="John Doe")
        self.material.subject = "Математика"

    def test_set_info(self):
        # Задаем информацию вручную, минуя вызов input
        self.material.subject = "Математика"
        self.material.topic = "Линейные уравнения"
        self.material.title = "Введение в алгебру"
        self.material.author = "John Doe"

        # Здесь можно вызвать метод save для сохранения материала
        self.material.save()

        # Проверяем, что информация установлена правильно
        self.assertEqual(self.material.subject, "Математика")
        self.assertEqual(self.material.topic, "Линейные уравнения")
        self.assertEqual(self.material.title, "Введение в алгебру")
        self.assertEqual(self.material.author, "John Doe")

    def test_save_and_load(self):
        self.material.save()
        loaded_material = EducationalMaterial.load("Линейные уравнения")
        self.assertIsNotNone(loaded_material)
        self.assertEqual(loaded_material.subject, "Математика")
        self.assertEqual(loaded_material.topic, "Линейные уравнения")
        self.assertEqual(loaded_material.title, "Введение в алгебру")
        self.assertEqual(loaded_material.author, "John Doe")

    def test_delete(self):
        self.material.save()
        self.material.delete()
        loaded_material = EducationalMaterial.load("Линейные уравнения")
        self.assertIsNone(loaded_material)

if __name__ == '__main__':
    unittest.main()