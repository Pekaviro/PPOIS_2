import tkinter as tk

from controller.controller import StudentController
from view.view import StudentView
from model.service import StudentModel
from model.repositories import InMemoryStudentRepository
from model.validators import BasicStudentValidator


def main():
    root = tk.Tk()
    root.title("Управление студентами")
    
    # Создаем цепочку зависимостей
    repository = InMemoryStudentRepository()
    validator = BasicStudentValidator()
    model = StudentModel(repository, validator)
    view = StudentView(root)
    controller = StudentController(model, view)
    
    root.mainloop()

if __name__ == "__main__":
    main()