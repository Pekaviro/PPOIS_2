import os
from abc import ABC, abstractmethod



class State(ABC):
    def __init__(self, console) -> None:
        self.console = console


    @abstractmethod
    def show_menu(self) -> None:
        pass


    @abstractmethod
    def handle_input(self, choice: str) -> None:
        pass



class InitialState(State):
    def show_menu(self) -> None:
        print("\n    Кто вы?")
        print("1. Студент.")
        print("2. Преподаватель.")
        print("0. Выход.")


    def handle_input(self, choice: str) -> None:
        try:
            if choice == "1":
                self.console.log_in()
                if self.console.student:
                    self.console.set_state(StudentState(self.console))
            elif choice == "2":
                self.console.set_state(TeacherState(self.console))
            elif choice == "0":
                exit()
            else:
                print("Неверное число!")
        except Exception as e:
            print(f"\nОшибка при обработке ввода: {e}")



class StudentState(State):
    def show_menu(self) -> None:
        print(f"\n     Главное меню")
        print("1. Анализ ошибок в прошлой сдаче.")
        print("2. Консультация с преподавателем.")
        print("3. Изучение дополнительной литературы.")
        print("4. Решение тренировочных тестов.")
        print("5. Повторная сдача экзамена.")
        print("0. Выход.")


    def handle_input(self, choice: str) -> None:
        try:
            if choice == "0":
                self.console.student = None
                self.console.set_state(InitialState(self.console))
                return

            self.console.process_student_choice(choice)
        except Exception as e:
            print(f"\nОшибка при обработке ввода: {e}")



class TeacherState(State):
    def show_menu(self) -> None:
        print(f"\n     Главное меню")
        print("1. Добавление.")
        print("2. Удаление.")
        print("0. Выход.")


    def handle_input(self, choice: str) -> None:
        try:
            if choice == "1":
                self.console.set_state(AddedState(self.console))
            elif choice == "2":
                self.console.set_state(DeletedState(self.console))
            elif choice == "0":
                self.console.student = None
                self.console.set_state(InitialState(self.console))
                return
            else:
                print("Неверное число!")
        except Exception as e:
            print(f"\nОшибка при обработке ввода: {e}")



class AddedState(State):
    def show_menu(self) -> None:
        print(f"\n     Добавить:")
        print("1. Студента.")
        print("2. Экзамен.")
        print("3. Дополнительную литературу.")
        print("0. Выход.")


    def handle_input(self, choice: str) -> None:
        try:
            if choice == "0":
                self.console.student = None
                self.console.set_state(TeacherState(self.console))
                return

            self.console.process_added_choice(choice)
        except Exception as e:
            print(f"\nОшибка при добавлении: {e}")



class DeletedState(State):
    def show_menu(self) -> None:
        print(f"\n     Удалить:")
        print("1. Студента.")
        print("2. Экзамен.")
        print("3. Дополнительную литературу.")
        print("0. Выход.")


    def handle_input(self, choice: str) -> None:
        try:
            if choice == "0":
                self.console.student = None
                self.console.set_state(TeacherState(self.console))
                return

            self.console.process_deleted_choice(choice)
        except Exception as e:
            print(f"\nОшибка при удалении: {e}")