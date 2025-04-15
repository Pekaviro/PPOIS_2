from typing import Dict, List
from tkinter import filedialog

from model.student import Student
from model.service import StudentModel


class StudentController:
    def __init__(self, model: StudentModel, view):
        self._model = model
        self._view = view
        self._view.set_controller(self)
        self._current_file_path = None
    
    def add_student(self, student_data: Dict[str, str]) -> bool:
        try:
            self._model.add_student(student_data)
            self._view.show_message("Студент добавлен!")
            self._view.update_view()
            return True
        except Exception as e:
            self._view.show_error(str(e))
            return False
    
    def delete_students(self, criteria: Dict[str, str]) -> None:
        try:
            deleted_count = self._model.delete_students(criteria)
            if deleted_count > 0:
                self._view.show_message(f"Удалено {deleted_count} записей.")
            else:
                self._view.show_message("Записи не найдены.")
            self._view.update_view()
        except Exception as e:
            self._view.show_error(f"Ошибка при удалении студентов: {e}")
    
    def save_to_file(self) -> None:
        file_path = self._current_file_path or filedialog.asksaveasfilename(
            defaultextension=".xml",
            filetypes=[("XML files", "*.xml")]
        )
        
        if not file_path:
            return
            
        try:
            self._model.save_to_file(file_path)
            self._current_file_path = file_path
            self._view.show_message("Данные успешно сохранены!")
        except Exception as e:
            self._view.show_error(f"Ошибка при сохранении данных: {e}")
    
    def load_from_file(self) -> None:
        file_path = filedialog.askopenfilename(filetypes=[("XML files", "*.xml")])
        if not file_path:
            return
            
        try:
            self._model.load_from_file(file_path)
            self._current_file_path = file_path
            self._view.show_message("Данные успешно загружены!")
            self._view.update_view()
        except Exception as e:
            self._view.show_error(f"Ошибка при загрузке данных: {e}")
    
    def get_paginated_students(self, page: int, page_size: int) -> List[Student]:
        try:
            return self._model.get_paginated_students(page, page_size)
        except Exception as e:
            self._view.show_error(f"Ошибка при получении данных: {e}")
            return []
    
    def get_total_students(self) -> int:
        return self._model.get_total_students()
    
    def get_search_results(self, criteria: Dict[str, str]) -> List[Student]:
        return self._model.search_students(criteria)
    
    def get_unique_values(self, field: str) -> List[str]:
        return self._model.get_unique_values(field)