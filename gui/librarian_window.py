import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from gui.add_book_window import AddBookWindow
from gui.reservations_window import ReservationsWindow


class LibrarianWindow(ttk.Toplevel):
    def __init__(self, master, user_id):
        super().__init__(master)
        self.master = master
        self.user_id = user_id
        self.title("Library System - Библиотекарь")
        self.state("zoomed")

        ttk.Label(
            self,
            text="Панель управления библиотекой",
            font=("Helvetica", 24),
            bootstyle="inverse-primary"
        ).pack(pady=20)

        button_frame = ttk.Frame(self, padding=20)
        button_frame.pack(expand=True)

        ttk.Button(
            button_frame,
            text="Добавить книгу",
            bootstyle="success",
            command=self.open_add_book_window,
            width=30
        ).pack(pady=10)

        ttk.Button(
            button_frame,
            text="Просмотреть бронирования",
            bootstyle="info",
            command=self.open_reservations_window,
            width=30
        ).pack(pady=10)

        ttk.Button(
            button_frame,
            text="Выйти",
            bootstyle="danger",
            command=self.exit_to_main,
            width=30
        ).pack(pady=10)

    def open_add_book_window(self):
        AddBookWindow(self)

    def open_reservations_window(self):
        ReservationsWindow(self)

    def exit_to_main(self):
        self.destroy()
        self.master.deiconify()
