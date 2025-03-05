from entities.educational_materials import EducationalMaterial
from entities.student import Student


class AdditionalClasses:
    def __init__(self, student: Student, topic: str):
        self.student: Student = student
        self.topic: str = topic

    def conduct_consultation(self) -> None:
        print(f"\nНачало консультации по теме '{self.topic}'.")

        try:
            self.recommend_literature()
        except Exception as e:
            print(f"Произошла ошибка во время консультации: {e}")
        finally:
            print("Консультация завершена.\n")

    def recommend_literature(self) -> None:
        try:
            material = EducationalMaterial(topic=self)
            materials = material.load_all()

            if self.topic in materials:
                material_data = materials[self.topic]
                recommended_material = EducationalMaterial(
                    topic=self.topic,
                    title=material_data['title'],
                    author=material_data['author']
                )

                # Инициализируем список материалов студента, если он пуст
                if self.student.materials is None:
                    self.student.materials = []

                # Проверяем, есть ли материал уже в списке студента
                is_material_exists = any(
                    book.topic == recommended_material.topic and
                    book.title == recommended_material.title and
                    book.author == recommended_material.author
                    for book in self.student.materials
                )

                if not is_material_exists:
                    self.student.materials.append(recommended_material)
                    print("\nРекомендованная литература:")
                    for book in self.student.materials:
                        print(f"- {book.title} (автор: {book.author})")

                    # Сохраняем изменения
                    self.student.save()
                else:
                    print("\nРекомендованная литература:")
                    for book in self.student.materials:
                        print(f"- {book.title} (автор: {book.author})")
            else:
                print("\nЛитература по данной теме не найдена.")
        except FileNotFoundError:
            print("\nОшибка: файл с учебными материалами не найден.")
        except Exception as e:
            print(f"\nПроизошла ошибка при загрузке литературы: {e}")
