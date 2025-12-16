from sys import stdin
from src.library_classes import Book, Library
from src.simulation import run_simulation

library = Library()


def add_book_interactive():
    try:
        title = input("Название книги: ").strip()
        author = input("Автор: ").strip()
        year = int(input("Год издания: ").strip())
        genre = input("Жанр: ").strip()
        isbn = input("ISBN: ").strip()
        
        book = Book(title, author, year, genre, isbn)
        library.add_book_to_lib(book)
        print(f"Книга '{title}' успешно добавлена")
    except ValueError:
        print("Ошибка: год издания должен быть числом")
    except Exception as e:
        print(f"Ошибка при добавлении книги: {e}")


def remove_book_interactive():
    try:
        isbn = input("Введите ISBN книги для удаления: ").strip()
        book = library.find_by_isbn(isbn)
        if book is None:
            print(f"Книга с ISBN '{isbn}' не найдена")
            return
        
        library.remove_book_from_lib(isbn)
        print(f"Книга '{book.title}' успешно удалена")
    except Exception as e:
        print(f"Ошибка при удалении книги: {e}")


def search_by_author_interactive():
    author = input("Введите имя автора: ").strip()
    books = library.find_by_author(author)
    
    if not books:
        print(f"Книг автора '{author}' не найдено")
    else:
        print(f"\nНайдено {len(books)} книг(и) автора '{author}':")
        for i, book in enumerate(books, 1):
            print(f"  {i}. {book.title} ({book.year}) - {book.genre}")


def search_by_year_interactive():
    try:
        year = int(input("Введите год издания: ").strip())
        books = library.find_by_year(year)
        
        if not books:
            print(f"Книг {year} года не найдено")
        else:
            print(f"\nНайдено {len(books)} книг(и) {year} года:")
            for i, book in enumerate(books, 1):
                print(f"  {i}. {book.title} ({book.author}) - {book.genre}")
    except ValueError:
        print("Ошибка: год должен быть числом")


def search_by_genre_interactive():
    genre = input("Введите жанр: ").strip()
    books = library.find_by_genre(genre)
    
    if not books:
        print(f"Книг жанра '{genre}' не найдено")
    else:
        print(f"\nНайдено {len(books)} книг(и) жанра '{genre}':")
        for i, book in enumerate(books, 1):
            print(f"  {i}. {book.title} ({book.author}, {book.year})")


def search_by_isbn_interactive():
    isbn = input("Введите ISBN: ").strip()
    book = library.find_by_isbn(isbn)
    
    if book is None:
        print(f"Книга с ISBN '{isbn}' не найдена")
    else:
        print(f"Название: {book.title}")
        print(f"Автор: {book.author}")
        print(f"Год: {book.year}")
        print(f"Жанр: {book.genre}")
        print(f"ISBN: {book.isbn}")


def update_book_interactive():
    try:
        isbn = input("Введите ISBN книги для обновления: ").strip()
        book = library.find_by_isbn(isbn)
        if book is None:
            print(f"Книга с ISBN '{isbn}' не найдена")
            return
        
        print(f"Текущая информация: {book}")
        print("\nВведите новые данные (оставьте пустым, чтобы не изменять):")
        
        title = input(f"Название [{book.title}]: ").strip()
        author = input(f"Автор [{book.author}]: ").strip()
        year_str = input(f"Год [{book.year}]: ").strip()
        genre = input(f"Жанр [{book.genre}]: ").strip()
        
        kwargs = {}
        if title:
            kwargs['title'] = title
        if author:
            kwargs['author'] = author
        if year_str:
            kwargs['year'] = int(year_str)
        if genre:
            kwargs['genre'] = genre
        
        if kwargs:
            library.update_book_info(isbn, **kwargs)
            print("Информация о книге обновлена")
        else:
            print("Изменения не внесены")
    except ValueError:
        print("Ошибка: год должен быть числом")
    except Exception as e:
        print(f"Ошибка при обновлении книги: {e}")


def list_all_books():
    if len(library) == 0:
        print("Библиотека пуста")
    else:
        print(f"Всего книг: {len(library)}\n")
        for i, book in enumerate(library, 1):
            print(f"{i}. {book.title} - {book.author} ({book.year})")


def simulation_interactive():
    try:
        steps_str = input("Введите количество шагов симуляции (по умолчанию 20): ").strip()
        steps = int(steps_str) if steps_str else 20
        
        seed_str = input("Введите seed для воспроизводимости (Enter для случайного): ").strip()
        seed = int(seed_str) if seed_str else None
        
        run_simulation(steps, seed)
    except ValueError:
        print("Error: некорректный ввод")
    except Exception as e:
        print(f"Ошибка при симуляции: {e}")


def main() -> None:
    print('Список команд для использования:\n'
          '1. Добавить книгу (исп.: add)\n'
          '2. Удалить книгу (исп.: remove)\n'
          '3. Поиск по автору (исп.: author)\n'
          '4. Поиск по году (исп.: year)\n'
          '5. Поиск по жанру (исп.: genre)\n'
          '6. Поиск по ISBN (исп.: isbn)\n'
          '7. Обновить книгу (исп.: update)\n'
          '8. Список всех книг (исп.: list)\n'
          '9. Запустить симуляцию (исп.: simulation)\n'
          'Для выхода напишите: "стоп!"')

    for cmd in stdin:
        try:
            cmd = cmd.strip()
            if cmd.lower() in ['стоп!', 'стоп', 'exit', 'quit']:
                break
            
            if not cmd:
                print('Введите команду')
                continue

            if cmd == 'add':
                add_book_interactive()
            elif cmd == 'remove':
                remove_book_interactive()
            elif cmd == 'author':
                search_by_author_interactive()
            elif cmd == 'year':
                search_by_year_interactive()
            elif cmd == 'genre':
                search_by_genre_interactive()
            elif cmd == 'isbn':
                search_by_isbn_interactive()
            elif cmd == 'update':
                update_book_interactive()
            elif cmd == 'list':
                list_all_books()
            elif cmd == 'simulation':
                simulation_interactive()
            else:
                print(f"Неизвестная команда: '{cmd}'. Введите одну из доступных команд.")
        
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Error: Ошибка при обработке команды: {e}")


if __name__ == "__main__":
    main()

