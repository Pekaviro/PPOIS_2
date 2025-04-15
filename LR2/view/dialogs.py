from abc import ABC, abstractmethod
import tkinter as tk
from tkinter import messagebox, ttk
from typing import List, Callable, Dict

from model.student import Student
from view.pagination import PaginatedView


class StudentDialog(ABC):
    def __init__(self, parent, controller, title: str):
        self._parent = parent
        self._controller = controller
        self._title = title
        self._dialog = None
    
    def show(self) -> None:
        self._dialog = tk.Toplevel(self._parent)
        self._dialog.title(self._title)
        self._dialog.grab_set()
        self._dialog.transient(self._parent)
        
        self._create_widgets()
    
    @abstractmethod
    def _create_widgets(self) -> None:
        pass
    
    def _show_message(self, message: str) -> None:
        messagebox.showinfo("Сообщение", message, parent=self._dialog)
    
    def _show_error(self, error: str) -> None:
        messagebox.showerror("Ошибка", error, parent=self._dialog)

class StudentSearchDialog(StudentDialog, PaginatedView):
    def __init__(self, parent, controller):
        StudentDialog.__init__(self, parent, controller, "Поиск студентов")
        PaginatedView.__init__(self)
        self._search_results = []
    
    def _create_widgets(self) -> None:
        self._dialog.geometry("1200x500")
        search_frame = ttk.Frame(self._dialog)
        search_frame.pack(fill='x', padx=10, pady=10)
        
        self._create_search_controls(search_frame)

        columns = ("FullName", "Course", "Group", "TotalWorks", "CompletedWorks", "ProgrammingLanguage")
        headings = ("ФИО", "Курс", "Группа", "Общее число работ", "Количество выполненных работ", "Язык программирования")
        
        self._table = ttk.Treeview(self._dialog, columns=columns, show="headings")
        for col, heading in zip(columns, headings):
            self._table.heading(col, text=heading)
            self._table.column(col, width=100)
        self._table.pack(fill='both', expand=True, padx=10, pady=5)

        self._create_pagination_controls(self._dialog)
    
    def _create_search_controls(self, parent) -> None:
        criteria_frame = ttk.Frame(parent)
        criteria_frame.pack(fill='x', pady=5)
        
        tk.Label(criteria_frame, text="Критерий:").pack(side='left', padx=(0, 10))
        values = ["ФИО", "Курс", "Группа", 
                 "Общее число работ", "Количество выполненных работ", 
                 "Количество не выполненных работ", "Язык программирования"]
        self._search_criteria = ttk.Combobox(criteria_frame, width=37, values=values)
        self._search_criteria.pack(side='left', fill='x', expand=True)
        self._search_criteria.set(values[0])
        
        self._value_frame = ttk.Frame(parent)
        self._value_frame.pack(fill='x', pady=5)
        
        self._search_value_var = tk.StringVar()
        self._search_value_widget = None
        
        self._search_criteria.bind("<<ComboboxSelected>>", self._on_criteria_select)
        self._on_criteria_select()
        
        tk.Button(parent, text="Найти", command=self._perform_search).pack(fill='x', pady=10)
    
    def _on_criteria_select(self, event=None) -> None:
        selected_criteria = self._search_criteria.get()
        
        for widget in self._value_frame.winfo_children():
            widget.destroy()
        
        self._search_value_var.set("")
        
        if selected_criteria in ["Язык программирования", "Общее число работ", "Количество выполненных работ"]:
            label = ttk.Label(self._value_frame, text=f"Выберите {selected_criteria.lower()}:")
            label.pack(side='left', padx=(0, 10))
            
            options = self._controller.get_unique_values(selected_criteria)
            
            self._search_value_widget = ttk.Combobox(
                self._value_frame, width=40, values=options, 
                state="readonly", textvariable=self._search_value_var
            )
            self._search_value_widget.pack(side='left', fill='x', expand=True)
            self._search_value_widget.set("(выберите значение из списка)")
        else:
            label = ttk.Label(self._value_frame, text=f"Введите {selected_criteria.lower()}:")
            label.pack(side='left', padx=(0, 10))
            
            self._search_value_widget = ttk.Entry(
                self._value_frame, width=40, textvariable=self._search_value_var
            )
            self._search_value_widget.pack(side='left', fill='x', expand=True)
    
    def _perform_search(self) -> None:
        criteria_map = {
            "ФИО": "FullName",
            "Курс": "Course",
            "Группа": "Group",
            "Язык программирования": "ProgrammingLanguage",
            "Общее число работ": "TotalWorks",
            "Количество выполненных работ": "CompletedWorks",
            "Количество не выполненных работ": "NotCompletedWorks"
        }
        
        criteria = self._search_criteria.get()
        value = self._search_value_var.get()
        
        if not criteria or not value:
            self._show_error("Заполните все поля!")
            return
        
        try:
            if criteria not in criteria_map:
                raise ValueError(f"Неизвестный критерий поиска: {criteria}")
                
            self._search_results = self._controller.get_search_results({criteria_map[criteria]: value})
            self._current_page = 1
            self.update_view()
            
            if not self._search_results:
                self._show_message("Студенты с указанными критериями не найдены")
        except Exception as e:
            self._show_error(f"Ошибка поиска: {e}")
    
    def update_view(self) -> None:
        self._table.delete(*self._table.get_children())
        self._total_items = len(self._search_results)
        
        start_index = (self._current_page - 1) * self._page_size
        end_index = start_index + self._page_size
        paginated_results = self._search_results[start_index:end_index]
        
        for student in paginated_results:
            self._table.insert("", "end", values=(
                student.full_name,
                student.course,
                student.group,
                student.total_works,
                student.completed_works,
                student.programming_language
            ))
        
        self._update_pagination_controls()

class StudentAddDialog(StudentDialog):
    def __init__(self, parent, controller):
        super().__init__(parent, controller, "Добавить студента")
    
    def _create_widgets(self) -> None:
        self._dialog.geometry("400x200")

        fields = ["ФИО", "Курс", "Группа", "Общее число работ", "Количество выполненных работ", "Язык программирования"]
        self._entries = {}
        
        for i, field in enumerate(fields):
            tk.Label(self._dialog, text=field).grid(row=i, column=0)
            entry = tk.Entry(self._dialog)
            entry.grid(row=i, column=1)
            self._entries[field] = entry
        
        tk.Button(self._dialog, text="Сохранить", command=self._save_student).grid(row=len(fields), column=0, columnspan=2)
    
    def _save_student(self) -> None:
        student_data = {
            "FullName": self._entries["ФИО"].get(),
            "Course": self._entries["Курс"].get(),
            "Group": self._entries["Группа"].get(),
            "TotalWorks": self._entries["Общее число работ"].get(),
            "CompletedWorks": self._entries["Количество выполненных работ"].get(),
            "ProgrammingLanguage": self._entries["Язык программирования"].get()
        }
        
        for field, value in student_data.items():
            if not value.strip():
                self._show_error("Заполните все поля!")
                return
        
        numeric_fields = {
            "Course": "Курс",
            "TotalWorks": "Общее число работ",
            "CompletedWorks": "Количество выполненных работ"
        }
        
        for field, display_name in numeric_fields.items():
            try:
                int(student_data[field])
            except ValueError:
                self._show_error(f"Поле '{display_name}' должно содержать целое число")
                return
        
        try:
            if self._controller.add_student(student_data):
                self._dialog.destroy()
        except Exception as e:
            self._show_error(str(e))          

class StudentDeleteDialog(StudentDialog):
    def __init__(self, parent, controller):
        super().__init__(parent, controller, "Удаление студентов")
    
    def _create_widgets(self) -> None:
        self._dialog.geometry("400x200")
        tk.Label(self._dialog, text="Критерий удаления:").pack()

        values=["ФИО", "Курс", "Группа", "Общее число работ", "Количество выполненных работ", "Количество не выполненных работ", "Язык программирования"]
        
        self._delete_criteria = ttk.Combobox(
            self._dialog, width=37, 
            values=values
        )
        self._delete_criteria.pack()
        self._delete_criteria.set(values[0])
        
        tk.Label(self._dialog, text="Значение:").pack()
        self._delete_value = tk.Entry(self._dialog, width=40)
        self._delete_value.pack()
        
        self._delete_criteria.bind("<<ComboboxSelected>>", self._clear_value)
        
        tk.Button(self._dialog, text="Удалить", command=self._perform_delete).pack()
    
    def _clear_value(self, event) -> None:
        self._delete_value.delete(0, tk.END)
    
    def _perform_delete(self) -> None:
        criteria_map = {
            "ФИО": "FullName",
            "Курс": "Course",
            "Группа": "Group",
            "Общее число работ": "TotalWorks",
            "Количество выполненных работ": "CompletedWorks",
            "Язык программирования": "ProgrammingLanguage",
            "Количество не выполненных работ": "NotCompletedWorks"
        }
        
        criteria = self._delete_criteria.get()
        value = self._delete_value.get()
        
        if not criteria or not value:
            self._show_error("Заполните все поля!")
            return
            
        try:
            self._controller.delete_students({criteria_map[criteria]: value})
            self._dialog.destroy()
        except Exception as e:
            self._show_error(f"Ошибка при удалении: {e}")