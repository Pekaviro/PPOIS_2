import json
import os
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple



class Exam:
    STORAGE_FILE = Path("storage/exams.json")

    def __init__(self, subject: Optional[str] = None) -> None:
        self.subject: str = subject
        self.questions: List[Tuple[str, str, str]] = []

    def set_info(self) -> None:
        try:
            self.subject = input("Введите название предмета: ").strip()
            if not self.subject:
                print("Название предмета не может быть пустым.")
                return

            # Проверка на дублирование экзамена
            exams = self.load_all()
            if self.subject in exams:
                print(f"Экзамен по предмету '{self.subject}' уже существует.")
                return

            # Инициализация списка для хранения вопросов
            self.questions = []

            # Цикл для ввода вопросов
            while True:
                print("\nВведите данные для нового вопроса (тема, вопрос, ответ).")
                topic = input("Введите тему: ").strip()
                if not topic:
                    print("Тема не может быть пустой.")
                    continue

                question = input("Введите вопрос: ").strip()
                if not question:
                    print("Вопрос не может быть пустым.")
                    continue

                answer = input("Введите ответ: ").strip()
                if not answer:
                    print("Ответ не может быть пустым.")
                    continue

                # Добавляем вопрос в список
                self.questions.append((topic, question, answer))

                # Спрашиваем, хочет ли пользователь добавить ещё один вопрос
                another = input("Хотите добавить ещё один вопрос? (да/нет): ").strip().lower()
                if another != "да":
                    break

            print("\nДанные экзамена успешно сохранены!")
            self.save()
        except Exception as e:
            print(f"Ошибка при вводе данных экзамена: {e}")

    @classmethod
    def display_exams(cls) -> None:
        try:
            exams = cls.load_all()
            print("\nСписок экзаменов:")
            for subject in exams.keys():
                print(f"- {subject}")
        except Exception as e:
            print(f"Ошибка при отображении списка экзаменов: {e}")

    @classmethod
    def load(cls, subject: str) -> Optional['Exam']:
        try:
            exams = cls.load_all()
            if subject not in exams:
                print(f"Экзамен по предмету '{subject}' не найден.")
                return None
            return cls.from_dict(exams[subject])
        except Exception as e:
            print(f"Ошибка при загрузке экзамена: {e}")
            return None

    @classmethod
    def load_all(cls) -> Dict[str, Dict[str, Any]]:
        try:
            if not cls.STORAGE_FILE.exists():
                return {}
            with open(cls.STORAGE_FILE, 'r', encoding='utf-8') as file:
                return json.load(file)
        except json.JSONDecodeError:
            print("Ошибка: Файл с экзаменами поврежден или имеет неверный формат.")
            return {}
        except FileNotFoundError:
            print("Ошибка: Файл с экзаменами не найден.")
            return {}
        except Exception as e:
            print(f"Неизвестная ошибка при загрузке экзаменов: {e}")
            return {}

    def save(self) -> None:
        try:
            exams = self.load_all()
            exams[self.subject] = self.to_dict()
            self.save_all(exams)
            print(f"Экзамен по предмету '{self.subject}' успешно сохранён.")
        except Exception as e:
            print(f"Ошибка при сохранении экзамена: {e}")

    @classmethod
    def save_all(cls, exams: Dict[str, Dict[str, Any]]) -> None:
        try:
            os.makedirs(cls.STORAGE_FILE.parent, exist_ok=True)
            with open(cls.STORAGE_FILE, 'w', encoding='utf-8') as file:
                json.dump(exams, file, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Ошибка при сохранении файла с экзаменами: {e}")

    def delete(self) -> None:
        try:
            exams = self.load_all()
            if self.subject in exams:
                del exams[self.subject]
                self.save_all(exams)
                print(f"Экзамен по предмету '{self.subject}' удалён из системы.")
            else:
                print(f"Экзамен по предмету '{self.subject}' не найден.")
        except Exception as e:
            print(f"Ошибка при удалении экзамена: {e}")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "subject": self.subject,
            "questions": [tuple(question) for question in self.questions]  # Преобразуем вопросы в кортежи
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Exam':
        exam = cls(subject=data.get('subject'))
        exam.questions = [tuple(question) for question in data.get('questions', [])]  # Преобразуем вопросы в кортежи
        return exam
