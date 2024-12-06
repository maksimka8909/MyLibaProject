import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
from database.config import SessionLocal
from database.models import Book, BorrowRecord, StatusEnum
from sqlalchemy import or_


class UserWindow(ttk.Toplevel):
    def __init__(self, master, user_id):
        super().__init__(master)
        self.master = master
        self.user_id = user_id
        self.title("Library System - Пользователь")
        self.state("zoomed")

        ttk.Label(
            self,
            text="Каталог книг",
            font=("Helvetica", 24),
            bootstyle="inverse-primary"
        ).pack(pady=20)

        search_frame = ttk.Frame(self, padding=10)
        search_frame.pack(fill=X, padx=20)

        ttk.Label(search_frame, text="Поиск:", font=("Helvetica", 14)).pack(side=LEFT, padx=(0, 10))
        self.search_entry = ttk.Entry(search_frame, font=("Helvetica", 12), width=50)
        self.search_entry.pack(side=LEFT, padx=(0, 10))

        ttk.Button(
            search_frame,
            text="Искать",
            bootstyle="success",
            command=self.search_books
        ).pack(side=LEFT)

        columns = ("Книга", "Автор", "Жанр", "Количество")
        self.books_table = ttk.Treeview(
            self, columns=columns, show="headings", height=15, bootstyle="info"
        )
        for col in columns:
            self.books_table.heading(col, text=col)
            self.books_table.column(col, width=200, anchor="center")
        self.books_table.pack(padx=20, pady=10, expand=True, fill=BOTH)

        button_frame = ttk.Frame(self, padding=10)
        button_frame.pack(fill=X, padx=20, pady=(10, 20))

        ttk.Button(
            button_frame,
            text="Забронировать",
            bootstyle="success",
            command=self.reserve_book
        ).pack(side=LEFT, padx=(0, 10))

        ttk.Button(
            button_frame,
            text="Выйти",
            bootstyle="danger",
            command=self.exit_to_main
        ).pack(side=LEFT)

        self.load_books()

    def load_books(self):
        session = SessionLocal()
        books = session.query(Book).all()
        session.close()

        for row in self.books_table.get_children():
            self.books_table.delete(row)

        for book in books:
            self.books_table.insert(
                "", "end", values=(book.title, book.author, book.genre, book.quantity)
            )

    def search_books(self):
        search_query = self.search_entry.get().strip()

        if not search_query:
            messagebox.showerror("Ошибка", "Введите текст для поиска.")
            return

        session = SessionLocal()
        try:
            books = session.query(Book).filter(
                or_(
                    Book.title.ilike(f"%{search_query}%"),
                    Book.author.ilike(f"%{search_query}%"),
                    Book.genre.ilike(f"%{search_query}%")
                )
            ).all()

            for row in self.books_table.get_children():
                self.books_table.delete(row)

            if not books:
                self.books_table.insert("", "end", values=("Результатов не найдено", "", "", ""))
            else:
                for book in books:
                    self.books_table.insert(
                        "", "end", values=(book.title, book.author, book.genre, book.quantity)
                    )
        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла ошибка: {str(e)}")
        finally:
            session.close()

    def reserve_book(self):
        selected_item = self.books_table.focus()
        if not selected_item:
            messagebox.showerror("Ошибка", "Выберите книгу для бронирования.")
            return

        book_info = self.books_table.item(selected_item, "values")
        book_title = book_info[0]

        session = SessionLocal()
        try:
            book = session.query(Book).filter_by(title=book_title).first()

            if book and book.quantity > 0:
                existing_record = session.query(BorrowRecord).filter_by(
                    user_id=self.user_id, book_id=book.id, status=StatusEnum.borrowed
                ).first()

                if existing_record:
                    messagebox.showerror("Ошибка", "Вы уже забронировали эту книгу.")
                    return

                # Обновляем количество и добавляем запись бронирования
                book.quantity -= 1
                borrow_record = BorrowRecord(user_id=self.user_id, book_id=book.id, status=StatusEnum.borrowed)
                session.add(borrow_record)
                session.commit()
                messagebox.showinfo("Успех", "Книга успешно забронирована!")
            else:
                messagebox.showerror("Ошибка", "Книга недоступна для бронирования.")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка бронирования: {str(e)}")
        finally:
            session.close()
            self.load_books()

    def exit_to_main(self):
        self.destroy()
        self.master.deiconify()
