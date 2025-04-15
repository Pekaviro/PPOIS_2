from abc import ABC, abstractmethod
from typing import Dict

class StudentValidator(ABC):
    @abstractmethod
    def validate(self, student_data: Dict[str, str]) -> None:
        pass

class BasicStudentValidator(StudentValidator):
    def validate(self, student_data: Dict[str, str]) -> None:
        required_fields = ["FullName", "Course", "Group", "TotalWorks", "CompletedWorks", "ProgrammingLanguage"]
        for field in required_fields:
            if field not in student_data or not str(student_data[field]).strip():
                raise ValueError(f"Отсутствует обязательное поле: {field}")

        try:
            course = int(student_data["Course"])
            if not 1 <= course <= 4:
                raise ValueError("Курс должен быть от 1 до 4")
            
            total = int(student_data["TotalWorks"])
            completed = int(student_data["CompletedWorks"])
            if total < 0 or completed < 0:
                raise ValueError("Количество работ должно быть неотрицательным")
            if completed > total:
                raise ValueError("Выполненных работ не может быть больше общего количества")
            
            parts = student_data["FullName"].split()
            if len(parts) != 3 or not all(part.isalpha() for part in parts):
                raise ValueError("ФИО должно содержать ровно 3 слова")
                
        except ValueError as e:
            raise ValueError(str(e))