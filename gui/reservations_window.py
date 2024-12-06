import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
from database.config import SessionLocal
from database.models import BorrowRecord, Book, User, StatusEnum


class ReservationsWindow(ttk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.title("Library System - Список бронирований")
        self.state("zoomed")


        ttk.Label(
            self,
            text="Список бронирований",
            font=("Helvetica", 24),
            bootstyle="inverse-primary"
        ).pack(pady=20)

        search_frame = ttk.Frame(self, padding=10)
        search_frame.pack(fill=X, padx=20)

        ttk.Label(search_frame, text="Поиск по пользователю:", font=("Helvetica", 16)).pack(side=LEFT, padx=(0, 10))
        self.search_entry = ttk.Entry(search_frame, font=("Helvetica", 14), width=50)
        self.search_entry.pack(side=LEFT, padx=(0, 10))

        ttk.Button(
            search_frame,
            text="Искать",
            bootstyle="success",
            command=self.search_reservations
        ).pack(side=LEFT)

        columns = ("Книга", "Пользователь", "Дата")
        self.reservations_table = ttk.Treeview(
            self, columns=columns, show="headings", height=15, bootstyle="info"
        )
        for col in columns:
            self.reservations_table.heading(col, text=col)
            self.reservations_table.column(col, width=200, anchor="center")
        self.reservations_table.pack(padx=20, pady=10, expand=True, fill=BOTH)

        button_frame = ttk.Frame(self, padding=20)
        button_frame.pack(fill=X, padx=20)

        ttk.Button(
            button_frame,
            text="Снять бронь",
            bootstyle="warning",
            command=self.cancel_reservation,
            width=20
        ).pack(side=LEFT, padx=10)

        ttk.Button(
            button_frame,
            text="Закрыть",
            bootstyle="danger",
            command=self.close_window,
            width=20
        ).pack(side=LEFT, padx=10)

        self.load_reservations()

    def load_reservations(self):
        session = SessionLocal()
        reservations = session.query(BorrowRecord).join(Book).join(User).filter(
            BorrowRecord.status == StatusEnum.borrowed
        ).all()
        session.close()

        # Очистка таблицы
        for row in self.reservations_table.get_children():
            self.reservations_table.delete(row)

        # Заполнение таблицы бронированиями
        for record in reservations:
            self.reservations_table.insert(
                "", "end",
                values=(record.book.title, record.user.name, record.borrow_date.strftime("%Y-%m-%d"))
            )

    def search_reservations(self):
        search_query = self.search_entry.get().strip()

        if not search_query:
            messagebox.showerror("Ошибка", "Введите текст для поиска.")
            return

        session = SessionLocal()
        try:
            reservations = session.query(BorrowRecord).join(Book).join(User).filter(
                User.name.ilike(f"%{search_query}%"),
                BorrowRecord.status == StatusEnum.borrowed
            ).all()

            for row in self.reservations_table.get_children():
                self.reservations_table.delete(row)

            for record in reservations:
                self.reservations_table.insert(
                    "", "end",
                    values=(record.book.title, record.user.name, record.borrow_date.strftime("%Y-%m-%d"))
                )
        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла ошибка: {str(e)}")
        finally:
            session.close()

    def cancel_reservation(self):
        selected_item = self.reservations_table.focus()
        if not selected_item:
            messagebox.showerror("Ошибка", "Выберите бронирование для снятия.")
            return

        reservation_info = self.reservations_table.item(selected_item, "values")
        book_title = reservation_info[0]
        user_name = reservation_info[1]

        session = SessionLocal()
        try:
            reservation = session.query(BorrowRecord).join(Book).join(User).filter(
                Book.title == book_title,
                User.name == user_name,
                BorrowRecord.status == StatusEnum.borrowed
            ).first()

            if reservation:
                reservation.status = StatusEnum.returned
                reservation.book.quantity += 1
                session.commit()
                messagebox.showinfo("Успех", "Бронь успешно снята!")
            else:
                messagebox.showerror("Ошибка", "Бронирование не найдено.")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла ошибка: {str(e)}")
        finally:
            session.close()
            self.load_reservations()

    def close_window(self):
        self.destroy()
