class Student:
    def __init__(self, full_name: str, course: int, group: str, 
                 total_works: int, completed_works: int, programming_language: str):
        self._full_name = full_name
        self._course = course
        self._group = group
        self._total_works = total_works
        self._completed_works = completed_works
        self._programming_language = programming_language

    @property
    def full_name(self) -> str:
        return self._full_name

    @property
    def course(self) -> int:
        return self._course

    @property
    def group(self) -> str:
        return self._group

    @property
    def total_works(self) -> int:
        return self._total_works

    @property
    def completed_works(self) -> int:
        return self._completed_works

    @property
    def programming_language(self) -> str:
        return self._programming_language

    @property
    def not_completed_works(self) -> int:
        return self._total_works - self._completed_works

    def __str__(self):
        return (f"Student(full_name={self._full_name}, course={self._course}, group={self._group}, "
                f"total_works={self._total_works}, completed_works={self._completed_works}, "
                f"programming_language={self._programming_language})")