# Модель подготовки к пересдаче экзамена

Модель подготовки к пересдаче экзамена фокусируется на повторной подготовке студентов после неудачной попытки сдачи. Она включает анализ ошибок в предыдущих попытках, дополнительное изучение материала, консультации с преподавателем, проведение тренировочных тестов и повторную сдачу экзамена.

## Классы

### Exam
Класс, представляющий экзамен.

**Атрибуты**:
  - `subject`: Дисциплина, по которой проводится экзамен.
  - `questions`: Список вопросов с соответствующими темами и правильными ответами.
  
**Методы**:
  - `set_info(self) -> None`: Заполнение информации об экзамене.
  - `display_exams(cls) -> None`: Выводит в коммандную строку список доступных экзаменов.
  - `load(cls, subject: str) -> Optional['Exam']`: Загрузка информации об экзамене по определённому предмету.
  - `load_all(cls) -> Dict[str, Dict[str, Any]]`: Загрузка информации обо всех экзаменах в файле.
  - `save(self) -> None`: Сохранение информации об экзамене.
  - `save_all(cls, exams: Dict[str, Dict[str, Any]]) -> None`: Сохранение информации обо всех экзаменах в файл.
  - `delete(self) -> None`: Удаление экзамена из файла.
  - `to_dict(self) -> Dict[str, Any]`: Запись информации об экзамене в словарик.
  - `from_dict(cls, data: Dict[str, Any]) -> 'Exam'`: Создание экземпляра класса на основе данных из словарика.  

### EducationalMaterial
Класс, представляющий учебный материал.

**Атрибуты**:
  - `subject`: Дисциплина, к которой относится учебный материал.
  - `topic`: Тема учебного материала.
  - `title`: Название учебного материала.
  - `author`: Автор учебного материала.

**Методы**:
  - `set_info(self) -> None`: Метод для ввода данных учебного материала.
  - `load(cls, topic: str) -> Optional['EducationalMaterial']`: Метод для загрузки учебного материала по теме.
  - `load_all(cls) -> Dict[str, Dict[str, Any]]`: Метод для загрузки всех учебных материалов из файла.
  - `save(self) -> None`: Метод для сохранения учебного материала.
  - `save_all(cls, materials: Dict[str, Dict[str, Any]]) -> None`: Метод для сохранения всех учебных материалов в файл.
  - `delete(self) -> None`: Метод для удаления учебного материала.
  - `to_dict(self) -> Dict[str, Any]`: Метод для преобразования объекта в словарь.
  - `from_dict(cls, data: Dict[str, Any]) -> 'EducationalMaterial'`: Метод для создания объекта из словаря.

### Student
Класс, представляющий студента.

**Атрибуты**:
  - `id`: Номер студенческого билета.
  - `last_name`: Фамилия студента.
  - `first_name`: Имя студента.
  - `exam_result`: Результаты предыдущей сдачи экзамена.
  - `materials`: Список учебных материалов для студента.
  - `unexplored_topics`: Список неизученных тем.

**Методы**:
  - `set_info(self) -> None`: Метод для ввода данных студента.
  - `set_exam_result(self) -> Optional[PreviousExamAttempt]`: Метод для ввода результатов экзамена.
  - `analyze_errors(self) -> List[Tuple[int, str, str, str, str]]`: Метод для анализа ошибок в результатах экзамена.
  - `display_errors(self) -> None`: Метод для отображения ошибок студента.
  - `study_materials(self) -> None`: Метод для изучения учебных материалов по ошибкам.
  - `practice_test(self, num_questions: int = 3) -> None`: Метод для прохождения тренировочного теста.
  - `re_passing_the_exam(self) -> None`: Метод для повторной сдачи экзамена.
  - `load(cls, id: str) -> Optional['Student']`: Метод для загрузки данных студента по ID.
  - `load_all(cls) -> Dict[str, Dict[str, Any]]`: Метод для загрузки всех данных студентов из файла.
  - `save(self) -> None`: Метод для сохранения данных студента.
  - `save_all(cls, students_data: Dict[str, Dict[str, Any]]) -> None`: Метод для сохранения всех данных студентов в файл.
  - `delete(self) -> None`: Метод для удаления данных студента.
  - `id_exist(cls, id: str) -> bool`: Метод для проверки существования студента по ID.
  - `to_dict(self) -> Dict[str, Any]`: Метод для преобразования объекта студента в словарь.
  - `from_dict(cls, data: Dict[str, Any]) -> 'Student'`: Метод для создания объекта студента из словаря.
  - `display_unexplored_topics(self) -> None`: Метод для отображения списка неизученных тем студента.

### PreviousExamAttempt
Класс, представляющий попытку сдачи экзамена.

**Атрибуты**:
  - `exam`: Экзамен, который сдавался.
  - `answers`: Список ответов студента на вопросы экзамена.

**Методы**:
  - `to_dict(self) -> Dict[str, Any]`: Метод для преобразования объекта в словарь.
  - `from_dict(cls, data: Dict[str, Any]) -> 'PreviousExamAttempt'`: Метод для создания объекта из словаря.
  - `calculate_score(self) -> int`: Метод для подсчета правильных ответов.
  - `display_results(self) -> None`: Метод для отображения результатов попытки сдачи экзамена.

### AdditionalClasses
Класс, представляющий дополнительные занятия.

**Атрибуты**:
  - `student`: Студент, для которого проводятся дополнительные занятия.
  - `topic`: Тема дополнительных занятий.

**Методы**:
  - `conduct_consultation(self) -> None`: Метод для проведения консультации.
  - `recommend_literature(self) -> None`: Метод для рекомендации учебной литературы по теме.

### Console
Класс, представляющий интерфейс командной строки для взаимодействия со студентами и системой.

**Атрибуты**:
  - `student`: Текущий студент.
  - `state`: Текущее состояние интерфейса.
  - `exam`: Текущий экзамен.
  - `educational_material`: Текущий учебный материал.

**Методы**:
  - `set_state(self, state: State) -> None`: Метод для установки текущего состояния интерфейса.
  - `start(self) -> None`: Метод для запуска интерфейса командной строки.
  - `log_in(self) -> None`: Метод для входа в систему студента.
  - `process_student_choice(self, choice: str) -> None`: Метод для обработки выбора студента.
  - `process_added_choice(self, choice: str) -> None`: Метод для обработки добавления данных.
  - `process_deleted_choice(self, choice: str) -> None`: Метод для обработки удаления данных.

## Классы состояний

### State
Абстрактный базовый класс, представляющий состояние интерфейса.

**Атрибуты**:
  - `console`: Экземпляр класса Console.

**Методы**:
  - `show_menu(self) -> None`: Абстрактный метод для отображения меню состояния.
  - `handle_input(self, choice: str) -> None`: Абстрактный метод для обработки ввода пользователя.

### InitialState
Класс, представляющий начальное состояние интерфейса.

**Методы**:
  - `show_menu(self) -> None`: Метод для отображения начального меню.
  - `handle_input(self, choice: str) -> None`: Метод для обработки ввода пользователя в начальном состоянии.

### StudentState
Класс, представляющий состояние интерфейса для студентов.

**Методы**:
  - `show_menu(self) -> None`: Метод для отображения меню студента.
  - `handle_input(self, choice: str) -> None`: Метод для обработки ввода пользователя в состоянии студента.

### TeacherState
Класс, представляющий состояние интерфейса для преподавателей.

**Методы**:
  - `show_menu(self) -> None`: Метод для отображения меню преподавателя.
  - `handle_input(self, choice: str) -> None`: Метод для обработки ввода пользователя в состоянии преподавателя.

### AddedState
Класс, представляющий состояние интерфейса для добавления данных.

**Методы**:
  - `show_menu(self) -> None`: Метод для отображения меню добавления данных.
  - `handle_input(self, choice: str) -> None`: Метод для обработки ввода пользователя в состоянии добавления данных.

### DeletedState
Класс, представляющий состояние интерфейса для удаления данных.

**Методы**:
  - `show_menu(self) -> None`: Метод для отображения меню удаления данных.
  - `handle_input(self, choice: str) -> None`: Метод для обработки ввода пользователя в состоянии удаления данных.
