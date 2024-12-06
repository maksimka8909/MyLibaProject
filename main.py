from sqlalchemy.exc import OperationalError
from database.config import engine
from gui.main_window import MainWindow
from sqlalchemy import text
import ttkbootstrap as ttk

def initialize_database():
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        print("Успешное подключение к базе данных.")
    except OperationalError as e:
        print(f"Ошибка подключения к базе данных: {e}")


def main():
    # Создаём корневое окно с темой
    root = ttk.Window(themename="darkly")
    MainWindow(root)  # Передаём корневое окно в главное
    root.mainloop()  # Запускаем цикл событий

if __name__ == "__main__":
    initialize_database()
    main()
