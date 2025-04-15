from typing import List, Dict
from abc import ABC, abstractmethod
from xml.etree import ElementTree as ET
from xml.dom import minidom
import xml.sax

from model.student import Student


class StudentRepository(ABC):
    @abstractmethod
    def add_student(self, student: Student) -> None:
        pass
    
    @abstractmethod
    def search_students(self, criteria: Dict[str, str]) -> List[Student]:
        pass
    
    @abstractmethod
    def delete_students(self, criteria: Dict[str, str]) -> int:
        pass
    
    @abstractmethod
    def get_all_students(self) -> List[Student]:
        pass
    
    @abstractmethod
    def get_paginated_students(self, page: int, page_size: int) -> List[Student]:
        pass
    
    @abstractmethod
    def get_total_students(self) -> int:
        pass
    
    @abstractmethod
    def get_unique_values(self, field: str) -> List[str]:
        pass

class InMemoryStudentRepository(StudentRepository):
    def __init__(self, students: List[Student] = None):
        self._students = students or []
    
    def add_student(self, student: Student) -> None:
        self._students.append(student)
    
    def search_students(self, criteria: Dict[str, str]) -> List[Student]:
        result = []
        for student in self._students:
            match = True
            for key, value in criteria.items():
                if key == "FullName" and value.lower() not in student.full_name.lower():
                    match = False
                elif key == "Course" and int(value) != student.course:
                    match = False
                elif key == "Group" and value.lower() not in student.group.lower():
                    match = False
                elif key == "ProgrammingLanguage" and value.lower() not in student.programming_language.lower():
                    match = False
                elif key == "CompletedWorks" and int(value) != student.completed_works:
                    match = False
                elif key == "TotalWorks" and int(value) != student.total_works:
                    match = False
                elif key == "NotCompletedWorks" and int(value) != student.not_completed_works:
                    match = False
            if match:
                result.append(student)
        return result
    
    def delete_students(self, criteria: Dict[str, str]) -> int:
        students_to_delete = self.search_students(criteria)
        for student in students_to_delete:
            self._students.remove(student)
        return len(students_to_delete)
    
    def get_all_students(self) -> List[Student]:
        return self._students
    
    def get_paginated_students(self, page: int, page_size: int) -> List[Student]:
        start = (page - 1) * page_size
        end = start + page_size
        return self._students[start:end]
    
    def get_total_students(self) -> int:
        return len(self._students)
    
    def get_unique_values(self, field: str) -> List[None]:
        field_mapping = {
            "Язык программирования": lambda s: s.programming_language,
            "Общее число работ": lambda s: int(s.total_works),
            "Количество выполненных работ": lambda s: int(s.completed_works)
        }
        
        if field not in field_mapping:
            return []
            
        return sorted(list(set(field_mapping[field](student) for student in self._students)))