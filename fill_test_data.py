from database.config import SessionLocal
from database.models import User, Book, RoleEnum


def populate_test_data():
    session = SessionLocal()

    try:
        # Добавление тестовых пользователей с логинами в поле `name`
        users = [
            User(name="ivanov.i", role=RoleEnum.user, password="password1"),
            User(name="petrov.p", role=RoleEnum.user, password="password2"),
            User(name="smirnova.m", role=RoleEnum.user, password="password3"),
            User(name="kuznecova.a", role=RoleEnum.librarian, password="password4"),
            User(name="sokolov.d", role=RoleEnum.librarian, password="password5"),
        ]

        # Добавление тестовых книг
        books = [
            Book(title="Путешествие на Запад", author="У Чэнъэнь", genre="Приключения", year=1592, quantity=5),
            Book(title="Мастер и Маргарита", author="Михаил Булгаков", genre="Фантастика", year=1966, quantity=3),
            Book(title="Война и мир", author="Лев Толстой", genre="Исторический роман", year=1869, quantity=10),
            Book(title="1984", author="Джордж Оруэлл", genre="Антиутопия", year=1949, quantity=4),
            Book(title="Преступление и наказание", author="Фёдор Достоевский", genre="Роман", year=1866, quantity=7),
            Book(title="Гарри Поттер и философский камень", author="Дж. К. Роулинг", genre="Фэнтези", year=1997, quantity=6),
            Book(title="Анна Каренина", author="Лев Толстой", genre="Роман", year=1877, quantity=5),
            Book(title="Маленький принц", author="Антуан де Сент-Экзюпери", genre="Сказка", year=1943, quantity=8),
            Book(title="Шерлок Холмс: Этюд в багровых тонах", author="Артур Конан Дойл", genre="Детектив", year=1887, quantity=3),
            Book(title="Моби Дик", author="Герман Мелвилл", genre="Приключения", year=1851, quantity=2),
        ]

        # Добавление данных в сессию
        session.add_all(users)
        session.add_all(books)

        # Сохранение изменений
        session.commit()
        print("Тестовые данные успешно добавлены.")
    except Exception as e:
        session.rollback()
        print(f"Ошибка при добавлении тестовых данных: {e}")
    finally:
        session.close()


if __name__ == "__main__":
    populate_test_data()
