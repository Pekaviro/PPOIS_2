import json
import os
from pathlib import Path
from typing import Any, Dict, Optional



class EducationalMaterial:
    STORAGE_FILE = Path("storage/materials.json")

    def __init__(self, topic: Optional[str] = None, title: Optional[str] = None, author: Optional[str] = None) -> None:
        self.subject: Optional[str] = None
        self.topic: Optional[str] = topic
        self.title: Optional[str] = title
        self.author: Optional[str] = author

    def set_info(self) -> None:
        """Метод для ввода данных учебного материала."""
        try:
            self.subject = input("Введите название предмета: ").strip()
            if not self.subject:
                print("Название предмета не может быть пустым.")
                return

            self.topic = input("Введите тему: ").strip()
            if not self.topic:
                print("Тема не может быть пустой.")
                return

            # Проверка на дублирование материала
            materials = self.load_all()
            if self.topic in materials:
                print(f"Материал с темой '{self.topic}' уже существует.")
                return

            self.title = input("Введите название материала: ").strip()
            if not self.title:
                print("Название материала не может быть пустым.")
                return

            self.author = input("Введите автора материала: ").strip()
            if not self.author:
                print("Автор не может быть пустым.")
                return

            print("\nДанные учебного материала успешно сохранены!")
            self.save()
        except Exception as e:
            print(f"Ошибка при вводе данных учебного материала: {e}")

    @classmethod
    def load(cls, topic: str) -> Optional['EducationalMaterial']:
        """Метод для загрузки учебного материала по теме."""
        try:
            materials = cls.load_all()
            if topic not in materials:
                print(f"Материал с темой '{topic}' не найден.")
                return None
            return cls.from_dict(materials[topic])
        except Exception as e:
            print(f"Ошибка при загрузке учебного материала: {e}")
            return None

    @classmethod
    def load_all(cls) -> Dict[str, Dict[str, Any]]:
        try:
            if not cls.STORAGE_FILE.exists():
                return {}
            with open(cls.STORAGE_FILE, 'r', encoding='utf-8') as file:
                return json.load(file)
        except json.JSONDecodeError:
            print("Ошибка: Файл с учебными материалами поврежден или имеет неверный формат.")
            return {}
        except FileNotFoundError:
            print("Ошибка: Файл с учебными материалами не найден.")
            return {}
        except Exception as e:
            print(f"Неизвестная ошибка при загрузке учебных материалов: {e}")
            return {}

    def save(self) -> None:
        """Метод для сохранения учебного материала."""
        try:
            materials = self.load_all()
            materials[self.topic] = self.to_dict()
            self.save_all(materials)
            print(f"Учебный материал '{self.title}' успешно сохранён.")
        except Exception as e:
            print(f"Ошибка при сохранении учебного материала: {e}")

    @classmethod
    def save_all(cls, materials: Dict[str, Dict[str, Any]]) -> None:
        """Метод для сохранения всех учебных материалов в файл."""
        try:
            os.makedirs(os.path.dirname(cls.STORAGE_FILE), exist_ok=True)
            with open(cls.STORAGE_FILE, 'w', encoding='utf-8') as file:
                json.dump(materials, file, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Ошибка при сохранении файла с учебными материалами: {e}")

    def delete(self) -> None:
        """Метод для удаления учебного материала."""
        try:
            materials = self.load_all()
            if self.topic in materials:
                del materials[self.topic]
                self.save_all(materials)
                print(f"Учебный материал '{self.title}' удалён из системы.")
            else:
                print(f"Учебный материал с темой '{self.topic}' не найден.")
        except Exception as e:
            print(f"Ошибка при удалении учебного материала: {e}")

    def to_dict(self) -> Dict[str, Any]:
        """Метод для преобразования объекта в словарь."""
        return {
            "subject": self.subject,
            "topic": self.topic,
            "title": self.title,
            "author": self.author
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'EducationalMaterial':
        """Метод для создания объекта из словаря."""
        material = cls(topic=data['topic'])
        material.subject = data['subject']
        material.title = data['title']
        material.author = data['author']
        return material