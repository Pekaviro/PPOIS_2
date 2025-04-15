import os
from typing import Optional

from entities.additional_classes import AdditionalClasses
from entities.educational_materials import EducationalMaterial
from entities.exam import Exam

from .states import InitialState, State

from entities.student import Student



class Console:
    def __init__(self):
        self.student: Optional[Student] = None
        self.state: Optional[State] = None
        self.set_state(InitialState(self))
        self.exam: Optional[Exam] = None
        self.educational_material: Optional[EducationalMaterial] = None

    def set_state(self, state: State) -> None:
        self.state = state

    def start(self) -> None:
        while True:
            try:
                self.state.show_menu()
                choice = input("\nВыберите действие: ")
                self.state.handle_input(choice)
            except KeyboardInterrupt:
                print("\nПрограмма завершена.")
                break
            except Exception as e:
                print(f"\nПроизошла ошибка: {e}")

    def log_in(self):
        while True:
            try:
                id = input("Введите номер студенческого билета: ")
                if not Student.id_exist(id):
                    print("\nВаш номер не был найден в списке.")
                    return
                else:
                    student = Student.load(id)
                    self.student = student
                    return
            except Exception as e:
                print(f"\nОшибка при входе в систему: {e}")
                return

    def process_student_choice(self, choice: str) -> None:
        try:
            if choice == "1":
                self.student.display_errors()
            elif choice == "2":
                self.student.display_unexplored_topics()
                topic = input("Введите тему для консультации: ")
                if not topic:
                    raise ValueError("Фамилия не может быть пустой.")
                consultation = AdditionalClasses(self.student, topic)
                consultation.conduct_consultation()
            elif choice == "3":
                self.student.study_materials()
            elif choice == "4":
                self.student.practice_test()
            elif choice == "5":
                self.student.re_passing_the_exam()
            else:
                print("Неверное число!")
        except AttributeError:
            print("\nОшибка: данные студента не загружены.")
        except Exception as e:
            print(f"\nПроизошла ошибка: {e}")

    def process_added_choice(self, choice: str) -> None:
        try:
            if choice == "1":
                self.student = Student()
                self.student.set_info()
            elif choice == "2":
                self.exam = Exam()
                self.exam.set_info()
            elif choice == "3":
                self.educational_material = EducationalMaterial()
                self.educational_material.set_info()
            else:
                print("Неверное число!")
        except Exception as e:
            print(f"\nОшибка при добавлении: {e}")

    def process_deleted_choice(self, choice: str) -> None:
        try:
            if choice == "1":
                id = input("Введите студенческий номер для удаления: ")
                student = Student.load(id)
                student.delete()
            elif choice == "2":
                subject = input("Введите дисциплину экзамена для удаления: ")
                exam = Exam(subject)
                exam.delete()
            elif choice == "3":
                topic = input("Введите тему учебного материала для удаления: ")
                material = EducationalMaterial(topic)
                material.delete()
            else:
                print("Неверное число!")
        except Exception as e:
            print(f"\nОшибка при удалении: {e}")