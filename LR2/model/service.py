from typing import List, Dict
from xml.etree import ElementTree as ET
from xml.dom import minidom
import xml.sax

from model.repositories import StudentRepository
from model.validators import StudentValidator
from model.student import Student
from model.student_handler import SaxHandler, DomHandler


class StudentModel:
    def __init__(self, repository: StudentRepository, validator: StudentValidator):
        self._repository = repository
        self._validator = validator
    
    def add_student(self, student_data: Dict[str, str]) -> None:
        self._validator.validate(student_data)
        student_data["FullName"] = self._format_fio(student_data["FullName"])
        student = Student(
            full_name=student_data["FullName"],
            course=int(student_data["Course"]),
            group=student_data["Group"],
            total_works=int(student_data["TotalWorks"]),
            completed_works=int(student_data["CompletedWorks"]),
            programming_language=student_data["ProgrammingLanguage"]
        )
        self._repository.add_student(student)
    
    def search_students(self, criteria: Dict[str, str]) -> List[Student]:
        return self._repository.search_students(criteria)
    
    def delete_students(self, criteria: Dict[str, str]) -> int:
        return self._repository.delete_students(criteria)
    
    def get_paginated_students(self, page: int, page_size: int) -> List[Student]:
        return self._repository.get_paginated_students(page, page_size)
    
    def get_total_students(self) -> int:
        return self._repository.get_total_students()
    
    def get_unique_values(self, field: str) -> List[str]:
        return self._repository.get_unique_values(field)
    
    def save_to_file(self, file_path: str) -> None:
        handler = DomHandler()
        handler.write_students_to_file(self._repository.get_all_students(), file_path)
    
    def load_from_file(self, file_path: str) -> None:
        handler = SaxHandler()
        parser = xml.sax.make_parser()
        parser.setContentHandler(handler)
        parser.parse(file_path)

        self._repository._students = []
        
        for student_data in handler.students:
            self.add_student(student_data)
    
    @staticmethod
    def _format_fio(full_name: str) -> str:
        if not full_name:
            return full_name
        return ' '.join(word.capitalize() for word in full_name.split())