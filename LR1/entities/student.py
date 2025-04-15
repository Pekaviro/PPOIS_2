import json
import os
from pathlib import Path
import random
from typing import Any, Dict, List, Optional, Tuple, Set

from entities.exam import Exam

from .previous_exam_attempt import PreviousExamAttempt
from .educational_materials import EducationalMaterial



class Student:
    STORAGE_FILE = Path("storage/students.json")

    def __init__(self, id: Optional[str] = None) -> None:
        self.id: Optional[str] = id
        self.last_name: Optional[str] = None
        self.first_name: Optional[str] = None
        self.exam_result: Optional[PreviousExamAttempt] = None
        self.materials: Optional[List[EducationalMaterial]] = None
        self.unexplored_topics: Optional[Set[str]] = None

    def set_info(self) -> None:
        try:
            self.id = input("Введите номер студенческого билета: ").strip()
            if not self.id:
                raise ValueError("Номер студенческого билета не может быть пустым.")
            if not self.id.isdigit():
                raise ValueError("Номер студенческого билета может содержать только цифры!")

            # Проверка на дублирование студента
            if self.id_exist(self.id):
                print(f"Студент с номером '{self.id}' уже существует.")
                return

            self.last_name = input("Введите фамилию студента: ").strip().title()
            if not self.last_name:
                raise ValueError("Фамилия не может быть пустой.")
            if not self.last_name.isalpha():
                raise ValueError("Фамилия может содержать только буквы!")

            self.first_name = input("Введите имя студента: ").strip().title()
            if not self.first_name:
                raise ValueError("Имя не может быть пустым.")
            if not self.first_name.isalpha():
                raise ValueError("Имя может содержать только буквы!")

            
            self.exam_result = self.set_exam_result()
            if not self.exam_result:
                return
            self.materials = []
            self.unexplored_topics = set()

            self.save()
            print(f"Данные студента {self.last_name} {self.first_name} успешно сохранены.")
        except ValueError as ve:
            print(f"Ошибка ввода данных: {ve}")
        except Exception as e:
            print(f"Неизвестная ошибка: {e}")

    def set_exam_result(self) -> Optional[PreviousExamAttempt]:
        try:
            Exam.display_exams()

            subject = input("Введите название экзамена: ").strip().title()
            if not subject:
                raise ValueError("Название экзамена не может быть пустым.")

            # Загружаем экзамен
            exam = Exam.load(subject)
            if exam is None:
                print("Экзамен не найден. Пожалуйста, проверьте название и попробуйте снова.")
                return None

            # Запрашиваем ответы студента
            answers = []
            for topic, question, correct_answer in exam.questions:
                answer = input(f"Введите ответ на вопрос: {question}\n").strip()
                if not answer:
                    raise ValueError("Ответ не может быть пустым.")
                answers.append(answer)

            return PreviousExamAttempt(exam, answers)
        except Exception as e:
            print(f"Ошибка при вводе результатов экзамена: {e}")
            return None

    def analyze_errors(self) -> List[Tuple[int, str, str, str, str]]:
        """Метод для анализа ошибок в результатах экзамена."""
        errors = []

        if not self.exam_result or not self.exam_result.exam.questions:
            return errors

        for i, (topic, question, correct_answer) in enumerate(self.exam_result.exam.questions):
            student_answer = self.exam_result.answers[i]
            if student_answer != correct_answer:
                errors.append((i, question, topic, student_answer, correct_answer))
                self.unexplored_topics = set()
                self.unexplored_topics.add(topic)

        self.save()

        return errors

    def display_errors(self) -> None:
        """Метод для отображения ошибок студента."""
        try:
            errors = self.analyze_errors()
            if not errors:
                print(f"{self.last_name} {self.first_name} не допустил(а) ошибок на экзамене по {self.exam_result.exam.subject}.")
            else:
                print(f"Ошибки {self.last_name} {self.first_name} на экзамене по {self.exam_result.exam.subject}:")
                for error in errors:
                    print(f"Вопрос {error[0] + 1}: {error[1]}")
                    print(f"Тема: {error[2]}")
                    print(f"Ответ: {error[3]}")
                    print(f"Правильный ответ: {error[4]}")
                    print("")
        except Exception as e:
            print(f"Ошибка при отображении ошибок: {e}")

    def study_materials(self) -> None:
        """Метод для изучения учебных материалов по ошибкам."""
        try:
            if not self.materials:
                print("Нет рекомендованной литературы для изучения. Советуем посетить консультацию.")
                return

            matched_materials = False
            errors = self.analyze_errors()

            for error in errors:
                found_material = False
                for material in self.materials:
                    if error[2] == material.topic:
                        if self.unexplored_topics:
                            self.unexplored_topics.discard(material.topic)
                        print(f"{self.last_name} {self.first_name} изучил(а) тему {material.topic} по литературе {material.title}.")
                        found_material = True
                        matched_materials = True

                if not found_material:
                    print(f"Для темы {error[2]} не найдена соответствующая литература.")

            if not matched_materials:
                print("Все ошибки проанализированы, но не найдена соответствующая дополнительная литература.")
        except Exception as e:
            print(f"Ошибка при изучении материалов: {e}")


    def practice_test(self, num_questions: int = 3) -> None:
        """Метод для прохождения тренировочного теста."""
        try:
            if not self.exam_result or not self.exam_result.exam.questions:
                print("Данные экзамена не загружены.")
                return

            questions_to_ask = random.sample(self.exam_result.exam.questions, min(num_questions, len(self.exam_result.exam.questions)))

            correct_answers = 0
            for topic, question, correct_answer in questions_to_ask:
                print(f"Вопрос: {question}")
                answer = input(f"\nВаш ответ: ").strip()
                if not answer:
                    raise ValueError("Ответ не может быть пустым.")
                correct_answer = correct_answer.strip()  # Удаление лишних пробелов
                if answer == correct_answer:
                    print("Правильно!")
                    correct_answers += 1
                else:
                    print(f"Неправильно. Правильный ответ: {correct_answer}")

            print(f"\nРезультат: {correct_answers} из {len(questions_to_ask)} правильных ответов.")
        except Exception as e:
            print(f"Ошибка при прохождении тренировочного теста: {e}")

    def re_passing_the_exam(self) -> None:
        """Метод для повторной сдачи экзамена."""
        try:
            if not self.exam_result or not self.exam_result.exam.questions:
                print("Данные экзамена не загружены.")
                return

            new_exam_result = PreviousExamAttempt(self.exam_result.exam, [])
            result = True

            for i, (topic, question, correct_answer) in enumerate(self.exam_result.exam.questions):
                answer = input(f"{question}\nВаш ответ: ").strip()
                if not answer:
                    raise ValueError("Ответ не может быть пустым.")

                new_exam_result.answers.append(answer)

                if correct_answer != new_exam_result.answers[i]:
                    result = False

            if result:
                print(f"{self.last_name} {self.first_name} сдал экзамен по {self.exam_result.exam.subject}.")
            else:
                print(f"{self.last_name} {self.first_name} не сдал экзамен по {self.exam_result.exam.subject}.")
            self.exam_result = new_exam_result
        except Exception as e:
            print(f"Ошибка при повторной сдаче экзамена: {e}")

    @classmethod
    def load(cls, id: str) -> Optional['Student']:
        try:
            students_data = cls.load_all()
            if id not in students_data:
                print(f"Студент с ID '{id}' не найден.")
                return None
            return cls.from_dict(students_data[id])
        except Exception as e:
            print(f"Ошибка при загрузке студента: {e}")
            return None

    @classmethod
    def load_all(cls) -> Dict[str, Dict[str, Any]]:
        """Метод для загрузки всех студентов из файла."""
        try:
            if not cls.STORAGE_FILE.exists():
                return {}
            with open(cls.STORAGE_FILE, 'r', encoding='utf-8') as file:
                return json.load(file)
        except json.JSONDecodeError:
            print("Ошибка: Файл с данными студентов поврежден или имеет неверный формат.")
            return {}
        except FileNotFoundError:
            print("Ошибка: Файл с данными студентов не найден.")
            return {}
        except Exception as e:
            print(f"Неизвестная ошибка при загрузке студентов: {e}")
            return {}

    def save(self) -> None:
        """Метод для сохранения данных студента."""
        try:
            students_data = self.load_all()
            students_data[self.id] = self.to_dict()
            self.save_all(students_data)
        except Exception as e:
            print(f"Ошибка при сохранении данных студента: {e}")

    @classmethod
    def save_all(cls, students_data: Dict[str, Dict[str, Any]]) -> None:
        """Метод для сохранения всех студентов в файл."""
        try:
            os.makedirs(os.path.dirname(cls.STORAGE_FILE), exist_ok=True)
            with open(cls.STORAGE_FILE, 'w', encoding='utf-8') as file:
                json.dump(students_data, file, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Ошибка при сохранении файла с данными студентов: {e}")

    def delete(self) -> None:
        try:
            students_data = self.load_all()
            if self.id in students_data:
                del students_data[self.id]
                self.save_all(students_data)
                print(f"Студент {self.last_name} {self.first_name} удален из системы.")
            else:
                print(f"Студент {self.last_name} {self.first_name} не найден!")
        except Exception as e:
            print(f"Ошибка при удалении студента: {e}")

    @classmethod
    def id_exist(cls, id: str) -> bool:
        """Метод для проверки существования студента по ID."""
        students = cls.load_all()
        return id in students

    def to_dict(self) -> Dict[str, Any]:
        """Метод для преобразования объекта в словарь."""
        materials_dict = None
        if self.materials:
            materials_dict = []
            for material in self.materials:
                if isinstance(material, EducationalMaterial):
                    materials_dict.append(material.to_dict())
                else:
                    print(f"Предупреждение: элемент {material} не является объектом EducationalMaterial.")

        return {
            "id": self.id,
            "last_name": self.last_name,
            "first_name": self.first_name,
            "exam_result": self.exam_result.to_dict() if self.exam_result else None,
            "materials": materials_dict,
            "unexplored_topics": list(self.unexplored_topics) if self.unexplored_topics else None
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Student':
        """Метод для создания объекта из словаря."""
        student = cls(id=data.get('id'))
        student.last_name = data.get('last_name')
        student.first_name = data.get('first_name')
        if 'exam_result' in data and data['exam_result']:
            student.exam_result = PreviousExamAttempt.from_dict(data['exam_result'])
        if 'materials' in data and data['materials']:
            student.materials = [EducationalMaterial.from_dict(material) for material in data['materials']]
        if 'unexplored_topics' in data and data['unexplored_topics']:
            student.unexplored_topics = set(data['unexplored_topics'])
        return student


    def display_unexplored_topics(self) -> None:
        try:
            if not self.unexplored_topics:
                print(f"{self.last_name} {self.first_name} изучил(а) все темы.")
                return

            print(f"\nСписок неизученных тем для {self.last_name} {self.first_name}:")
            for topic in self.unexplored_topics:
                print(f"- {topic}")
        except Exception as e:
            print(f"Ошибка при выводе списка неизученных тем: {e}")