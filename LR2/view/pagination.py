import tkinter as tk
from tkinter import ttk
from typing import List


class PaginatedView:
    def __init__(self):
        self._page_size = 10
        self._current_page = 1
        self._total_items = 0
        self.data = []
        
        # Элементы управления, которые должны быть созданы в дочерних классах
        self._table = None
        self._page_label = None
        self._prev_button = None
        self._next_button = None
        self._first_button = None
        self._last_button = None
        self._page_size_entry = None
    
    def _create_pagination_controls(self, parent) -> None:
        """Создает элементы управления пагинацией."""
        pagination_frame = tk.Frame(parent)
        pagination_frame.pack(fill='x', pady=5)
        
        # Page navigation controls
        page_controls = tk.Frame(pagination_frame)
        page_controls.pack(pady=5)
        
        self._first_button = tk.Button(page_controls, text="<<", command=self.first_page)
        self._first_button.grid(row=0, column=0, padx=2)
        
        self._prev_button = tk.Button(page_controls, text="<", command=self.prev_page)
        self._prev_button.grid(row=0, column=1, padx=2)
        
        self._page_label = tk.Label(page_controls, text="Страница: 1")
        self._page_label.grid(row=0, column=2, padx=5)
        
        self._next_button = tk.Button(page_controls, text=">", command=self.next_page)
        self._next_button.grid(row=0, column=3, padx=2)
        
        self._last_button = tk.Button(page_controls, text=">>", command=self.last_page)
        self._last_button.grid(row=0, column=4, padx=2)

        # Page size controls
        page_size_frame = ttk.Frame(pagination_frame)
        page_size_frame.pack(side='left', pady=5)
        
        tk.Label(page_size_frame, text="Записей на странице:").pack(side='left')
        self._page_size_entry = tk.Entry(page_size_frame, width=5)
        self._page_size_entry.insert(0, str(self._page_size))
        self._page_size_entry.pack(side='left', padx=5)
        
        tk.Button(page_size_frame, text="Изменить", command=self._change_page_size).pack(side='left')
        
        
        self._update_pagination_controls()
    
    def _update_pagination_controls(self) -> None:
        """Обновляет состояние элементов управления пагинацией."""
        total_pages = max(1, (self._total_items + self._page_size - 1) // self._page_size)
        
        if self._page_label:
            self._page_label.config(text=f"Страница: {self._current_page} из {total_pages}")
        
        if all(button is not None for button in [self._prev_button, self._next_button, 
                                              self._first_button, self._last_button]):
            self._prev_button['state'] = 'normal' if self._current_page > 1 else 'disabled'
            self._next_button['state'] = 'normal' if self._current_page < total_pages else 'disabled'
            self._first_button['state'] = 'normal' if self._current_page > 1 else 'disabled'
            self._last_button['state'] = 'normal' if self._current_page < total_pages else 'disabled'
    
    def _change_page_size(self) -> None:
        """Изменяет количество записей на странице."""
        try:
            new_page_size = int(self._page_size_entry.get())
            if new_page_size > 0:
                self._page_size = new_page_size
                self._current_page = 1
                self.update_view()
            else:
                self.show_error("Количество записей на странице должно быть больше 0.")
        except ValueError:
            self.show_error("Введите корректное число.")
    
    def first_page(self) -> None:
        """Переход на первую страницу."""
        if self._current_page != 1:
            self._current_page = 1
            self.update_view()
    
    def last_page(self) -> None:
        """Переход на последнюю страницу."""
        total_pages = max(1, (self._total_items + self._page_size - 1) // self._page_size)
        if self._current_page != total_pages:
            self._current_page = total_pages
            self.update_view()
    
    def prev_page(self) -> None:
        """Переход на предыдущую страницу."""
        if self._current_page > 1:
            self._current_page -= 1
            self.update_view()
    
    def next_page(self) -> None:
        """Переход на следующую страницу."""
        total_pages = max(1, (self._total_items + self._page_size - 1) // self._page_size)
        if self._current_page < total_pages:
            self._current_page += 1
            self.update_view()
    
    def update_view(self) -> None:
        """Обновляет отображение данных. Должен быть переопределен в дочерних классах."""
        raise NotImplementedError("Метод update_view должен быть реализован в дочернем классе")
    
    def show_error(self, error: str) -> None:
        """Показывает сообщение об ошибке. Должен быть переопределен в дочерних классах."""
        raise NotImplementedError("Метод show_error должен быть реализован в дочернем классе")