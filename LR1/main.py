#!/usr/bin/env python


# КАК ВЫВОДИТЬ В КОНСОЛЬ ЗНАЕТ ТОЛЬКО КАКОЙ-ТО ИНТЕРФЕЙС ОТДЕЛЬНЫЙ!!!!!!!!!!!!!


from console.console import Console


def main():
    console = Console()
    console.start()


if __name__ == "__main__":
    main()





# ПРИМЕР ИСПОЛЬЗОВАНИЯ ТАБЛИЦЫ ДЛЯ ХРАНЕНИЯ ЛИТЕРАТУРЫ
# для создания таких файлов можно использовать эксель и просто сохранить в нужном формате

# import csv

# def search_literature_by_topic(file_path, topic):
#     results = []
#     with open(file_path, mode='r', encoding='utf-8') as file:
#         reader = csv.DictReader(file)
#         for row in reader:
#             if topic.lower() in row['Тема'].lower():
#                 results.append(row)
#     return results

# # Пример использования
# file_path = 'literature_list.csv'
# topic = 'Алгоритмы и структуры данных'
# found_literature = search_literature_by_topic(file_path, topic)

# # Вывод результатов
# if found_literature:
#     for item in found_literature:
#         print(f"Тема: {item['Тема']}, Источник: {item['Источник']}, Автор: {item['Автор']}, Год: {item['Год']}, Аннотация: {item['Аннотация']}")
# else:
#     print("Литература по заданной теме не найдена.")