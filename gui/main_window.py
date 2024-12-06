import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
from database.config import SessionLocal
from database.models import User, RoleEnum
from gui.user_window import UserWindow
from gui.librarian_window import LibrarianWindow


class MainWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("Library System - Авторизация")
        self.master.state("zoomed")

        ttk.Label(
            master,
            text="Добро пожаловать в библиотечную систему",
            font=("Helvetica", 24),
            bootstyle="inverse-primary"
        ).pack(pady=20)

        ttk.Label(master, text="Логин:", font=("Helvetica", 14)).pack(pady=5)
        self.username_entry = ttk.Entry(master, bootstyle="info", font=("Helvetica", 12))
        self.username_entry.pack(pady=5)

        ttk.Label(master, text="Пароль:", font=("Helvetica", 14)).pack(pady=5)
        self.password_entry = ttk.Entry(master, bootstyle="info", font=("Helvetica", 12), show="*")
        self.password_entry.pack(pady=5)

        ttk.Button(
            master,
            text="Войти",
            bootstyle="success",
            command=self.login
        ).pack(pady=15)

        ttk.Button(
            master,
            text="Выход",
            bootstyle="danger",
            command=self.exit_app
        ).pack(pady=10)

    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            messagebox.showerror("Ошибка", "Введите логин и пароль.")
            return

        session = SessionLocal()
        user = session.query(User).filter_by(name=username, password=password).first()
        session.close()

        if user:
            messagebox.showinfo("Успех", "Добро пожаловать!")
            if user.role == RoleEnum.user:
                self.open_user_window(user.id)
            elif user.role == RoleEnum.librarian:
                self.open_librarian_window(user.id)
        else:
            messagebox.showerror("Ошибка", "Неверный логин или пароль.")

    def open_user_window(self, user_id):
        self.master.withdraw()
        UserWindow(self.master, user_id)

    def open_librarian_window(self, user_id):
        self.master.withdraw()
        LibrarianWindow(self.master, user_id)

    def exit_app(self):
        self.master.quit()
