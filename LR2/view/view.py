import tkinter as tk
from tkinter import messagebox, ttk

from view.dialogs import StudentAddDialog, StudentSearchDialog, StudentDeleteDialog
from view.pagination import PaginatedView


class StudentView(PaginatedView):
    def __init__(self, root):
        super().__init__()
        self._root = root
        self._controller = None
        
        self._create_ui()
    
    def set_controller(self, controller) -> None:
        self._controller = controller
    
    def _create_ui(self) -> None:
        self._create_control_frame()
        self._create_table()
        self._create_pagination_controls()
    
    def _create_control_frame(self) -> None:
        control_frame = ttk.Frame(self._root)
        control_frame.pack(fill='x', padx=10, pady=10)
        
        buttons = [
            ("Добавить", self.on_add_button_clicked),
            ("Поиск", self.on_search_button_clicked),
            ("Удалить", self.on_delete_button_clicked),
            ("Сохранить", self.on_save_button_clicked),
            ("Загрузить", self.on_load_button_clicked)
        ]
        
        for text, command in buttons:
            btn = tk.Button(control_frame, text=text, command=command)
            btn.pack(side='left', padx=5)
    
    def _create_table(self) -> None:
        columns = ("FullName", "Course", "Group", "TotalWorks", "CompletedWorks", "ProgrammingLanguage")
        headings = ("ФИО", "Курс", "Группа", "Общее число работ", "Количество выполненных работ", "Язык программирования")
        
        self._table = ttk.Treeview(self._root, columns=columns, show="headings")
        for col, heading in zip(columns, headings):
            self._table.heading(col, text=heading)
        self._table.pack(fill='both', expand=True)
    
    def _create_pagination_controls(self) -> None:
        super()._create_pagination_controls(self._root)
    
    def show_message(self, message: str) -> None:
        messagebox.showinfo("Сообщение", message)
    
    def show_error(self, error: str) -> None:
        messagebox.showerror("Ошибка", error)
    
    def update_view(self) -> None:
        self._table.delete(*self._table.get_children())
        students = self._controller.get_paginated_students(self._current_page, self._page_size)
        self._total_items = self._controller.get_total_students()
        
        for student in students:
            self._table.insert("", "end", values=(
                student.full_name,
                student.course,
                student.group,
                student.total_works,
                student.completed_works,
                student.programming_language
            ))
        
        self._update_pagination_controls()
    
    def on_add_button_clicked(self) -> None:
        dialog = StudentAddDialog(self._root, self._controller)
        dialog.show()
    
    def on_search_button_clicked(self) -> None:
        dialog = StudentSearchDialog(self._root, self._controller)
        dialog.show()
    
    def on_delete_button_clicked(self) -> None:
        dialog = StudentDeleteDialog(self._root, self._controller)
        dialog.show()
    
    def on_save_button_clicked(self) -> None:
        self._controller.save_to_file()
    
    def on_load_button_clicked(self) -> None:
        self._current_page = 1
        self._controller.load_from_file()
        self.update_view()