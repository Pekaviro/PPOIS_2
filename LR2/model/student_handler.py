import xml.sax
from tkinter import filedialog
from xml.dom import minidom
from typing import List, Dict

from model.student import Student


# Обработчик SAX
class SaxHandler(xml.sax.ContentHandler):
    def __init__(self):
        self.students = []
        self.current_student = None
        self.current_element = None

    def startElement(self, name, attrs):
        if name == "Student":
            self.current_student = {}
        self.current_element = name

    def characters(self, content):
        if self.current_element and content.strip():
            if self.current_element in ["FullName", "Group", "ProgrammingLanguage"]:
                self.current_student[self.current_element] = content
            elif self.current_element in ["Course", "TotalWorks", "CompletedWorks"]:
                self.current_student[self.current_element] = int(content)

    def endElement(self, name):
        if name == "Student":
            self.students.append(self.current_student)
        self.current_element = None


# Обработчик DOM
class DomHandler:
    def write_students_to_file(self, students: List[Student], file_path: str) -> None:
        """Сохраняет список студентов в XML-файл с использованием DOM."""
        doc = minidom.Document()
        root = doc.createElement("Students")
        doc.appendChild(root)

        for student in students:
            student_elem = doc.createElement("Student")
            
            self._add_text_element(doc, student_elem, "FullName", student.full_name)
            self._add_text_element(doc, student_elem, "Course", str(student.course))
            self._add_text_element(doc, student_elem, "Group", student.group)
            self._add_text_element(doc, student_elem, "TotalWorks", str(student.total_works))
            self._add_text_element(doc, student_elem, "CompletedWorks", str(student.completed_works))
            self._add_text_element(doc, student_elem, "ProgrammingLanguage", student.programming_language)
            
            root.appendChild(student_elem)

        with open(file_path, "w", encoding="utf-8") as file:
            file.write(doc.toprettyxml(indent="  "))
    
    def _add_text_element(self, doc, parent, name, text):
        """Создает текстовый элемент и добавляет его к родительскому."""
        elem = doc.createElement(name)
        elem.appendChild(doc.createTextNode(text))
        parent.appendChild(elem)      