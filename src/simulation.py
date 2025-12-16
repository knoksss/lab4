import random
from src.library_classes import Book, Library


# данные для генерации случайных книг
TITLES = ["Война и мир", "Преступление и наказание", "Мастер и Маргарита",
          "Анна Каренина", "Братья Карамазовы", "1984"]
AUTHORS = ["Лев Толстой", "Фёдор Достоевский", "Михаил Булгаков", "Джордж Оруэлл"]
GENRES = ["Роман", "Повесть", "Фантастика", "Классика"]

isbn_counter = 1000 # счётчик для генерации уникальных ISBN


def gen_isbn() -> str: # генерация уникального ISBN
    global isbn_counter
    isbn_counter += 1
    return f"978-5-{isbn_counter:05d}"


def gen_book() -> Book: # генерация случайной книги
    return Book(random.choice(TITLES), random.choice(AUTHORS),
                random.randint(1800, 2025), random.choice(GENRES), gen_isbn())


def run_simulation(steps=20, seed: int | None = None) -> None: # основная функция симуляции
    try:
        if seed is not None:
            random.seed(seed)
        # инициализация библиотеки
        library = Library()
        
        # основной цикл симуляции
        for step in range(1, steps + 1):
            event = random.choice(["add", "remove", "search_author", "search_year", "search_genre", "update", "get_none"])
            print(f"[Шаг {step}] {event}")
            
            if event == "add": # добавление книги
                book = gen_book()
                library.add_book_to_lib(book)
                print(f"Добавлена: '{book.title}'")
            
            elif event == "remove": # удаление книги
                if len(library) == 0:
                    print("Нет книг")
                else:
                    book = random.choice(list(library))
                    library.remove_book_from_lib(book.isbn)
                    print(f"Удалена: '{book.title}'")
            
            elif event == "search_author": # поиск по автору
                author = random.choice(AUTHORS)
                books = library.find_by_author(author)
                print(f"'{author}': {len(books)} книг")
            
            elif event == "search_year": # поиск по году
                year = random.randint(1800, 2025)
                books = library.find_by_year(year)
                print(f"Год {year}: {len(books)} книг")
            
            elif event == "search_genre": # поиск по жанру
                genre = random.choice(GENRES)
                books = library.find_by_genre(genre)
                print(f"'{genre}': {len(books)} книг")
            
            elif event == "update": # обновление информации о книге
                if len(library) > 0:
                    book = random.choice(list(library))
                    new_year = random.randint(1800, 2025)
                    library.update_book_info(book.isbn, year=new_year)
                    print(f"Обновлён год '{book.title}': {new_year}")
                else:
                    print("Нет книг")
            
            elif event == "get_none": # попытка найти несуществующую книгу
                book = library.find_by_isbn("978-0-00000")
                print(f"Книга не найдена: {book is None}")
        
        print(f"Симуляция завершена.")
        print(f"Книг: {len(library)}")
        for i, book in enumerate(list(library)[:3], 1): # вывод первых 3 книг
            print(f"  {i}. {book.title}")

    except Exception as e: # обработка ошибок
        print(f"Ошибка в симуляции: {e}")


if __name__ == "__main__":
    run_simulation(steps=20, seed=42) # запуск симуляции
