import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
from database.config import SessionLocal
from database.models import Book


class AddBookWindow(ttk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.title("Library System - Добавить книгу")
        self.state("zoomed")

        main_frame = ttk.Frame(self, padding=20)
        main_frame.pack(expand=True, fill=BOTH)

        ttk.Label(
            main_frame,
            text="Добавить новую книгу",
            font=("Helvetica", 28),
            bootstyle="inverse-primary"
        ).grid(row=0, column=0, columnspan=2, pady=(20, 40))

        ttk.Label(main_frame, text="Название книги:", font=("Helvetica", 16)).grid(row=1, column=0, sticky=E, pady=10, padx=20)
        self.title_entry = ttk.Entry(main_frame, font=("Helvetica", 16), width=40)
        self.title_entry.grid(row=1, column=1, pady=10, padx=20)

        ttk.Label(main_frame, text="Автор:", font=("Helvetica", 16)).grid(row=2, column=0, sticky=E, pady=10, padx=20)
        self.author_entry = ttk.Entry(main_frame, font=("Helvetica", 16), width=40)
        self.author_entry.grid(row=2, column=1, pady=10, padx=20)

        ttk.Label(main_frame, text="Жанр:", font=("Helvetica", 16)).grid(row=3, column=0, sticky=E, pady=10, padx=20)
        self.genre_entry = ttk.Entry(main_frame, font=("Helvetica", 16), width=40)
        self.genre_entry.grid(row=3, column=1, pady=10, padx=20)

        ttk.Label(main_frame, text="Год:", font=("Helvetica", 16)).grid(row=4, column=0, sticky=E, pady=10, padx=20)
        self.year_entry = ttk.Entry(main_frame, font=("Helvetica", 16), width=40)
        self.year_entry.grid(row=4, column=1, pady=10, padx=20)

        ttk.Label(main_frame, text="Количество:", font=("Helvetica", 16)).grid(row=5, column=0, sticky=E, pady=10, padx=20)
        self.quantity_entry = ttk.Entry(main_frame, font=("Helvetica", 16), width=40)
        self.quantity_entry.grid(row=5, column=1, pady=10, padx=20)

        button_frame = ttk.Frame(main_frame, padding=20)
        button_frame.grid(row=6, column=0, columnspan=2, pady=20)

        ttk.Button(
            button_frame,
            text="Сохранить",
            bootstyle="success",
            command=self.save_book,
            width=20
        ).pack(side=LEFT, padx=20)

        ttk.Button(
            button_frame,
            text="Отмена",
            bootstyle="danger",
            command=self.close_window,
            width=20
        ).pack(side=LEFT, padx=20)

        # Центрирование внутри основного окна
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)

    def save_book(self):
        """Сохраняет книгу в базу данных."""
        title = self.title_entry.get().strip()
        author = self.author_entry.get().strip()
        genre = self.genre_entry.get().strip()
        year = self.year_entry.get().strip()
        quantity = self.quantity_entry.get().strip()

        if not all([title, author, genre, year, quantity]):
            messagebox.showerror("Ошибка", "Заполните все поля.")
            return

        try:
            year = int(year)
            quantity = int(quantity)
        except ValueError:
            messagebox.showerror("Ошибка", "Год и количество должны быть числовыми.")
            return

        session = SessionLocal()
        try:
            new_book = Book(title=title, author=author, genre=genre, year=year, quantity=quantity)
            session.add(new_book)
            session.commit()
            messagebox.showinfo("Успех", "Книга успешно добавлена!")
            self.destroy()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла ошибка: {str(e)}")
        finally:
            session.close()

    def close_window(self):
        self.destroy()
