from typing import Iterator
from typing import Dict
from src.errors import ExistError


class Book:
    # инициализация книги с её данными
    def __init__(self, title: str, author: str, year: int, genre: str, isbn: str) -> None:
        self.title = title # название книги
        self.author = author # автор книги
        self.year = year # год издания
        self.genre = genre # жанр книги
        self.isbn = isbn # уникальный идентификатор книги


    def __repr__(self) -> str: # представление информации о книге
        return f'Книга: {self.title}, {self.author}, {self.year}, {self.genre}, {self.isbn}'
    

    def __str__(self):
        return f'Книга: {self.title}, {self.author}, {self.year}, {self.genre}, {self.isbn}'


    def __eq__(self, other: object) -> bool: # сравнение книг по isbn
        if not isinstance(other, Book):
            return False
        return self.isbn == other.isbn
    

class Magazine(Book): # журнал - наследник класса "книга"
    def __init__(self, title: str, author: str, year: int, number: int, month: str, genre: str = "Журнал", isbn: str = ""):
        super().__init__(title, author, year, genre, isbn)
        self.number = number # номер выпуска
        self.month = month # месяц выпуска
    

    def __repr__(self):
        return f"{self.title} - Выпуск {self.number}, {self.month} {self.year}"
    

    def get_info_magazine(self): # уникальный метод только для журнала
        return f"Выпуск {self.number} за {self.month} {self.year}"
        

class TrainigMaterial(Book): # методическое пособие - наследник класса "книга"
    def __init__(self, title: str, author: str, year: int, edu_institution: int,
                   readers: str, genre: str = "Методическое пособие", isbn: str = ""):
        super().__init__(title, author, year, genre, isbn)
        self.edu_institution = edu_institution # учебное заведение
        self.readers = readers # читатели


    def __repr__(self):
        return f"Методическое пособие {self.title} - {self.author}, {self.year}"
    

    def get_info_training_material(self): # уникальный метод только для методического пособия
        return f"Методическое пособие {self.title} : учебное заведение - {self.edu_institution} - {self.author}"


class BookCollection: # коллекция книг
    def __init__(self, books: None | list = None) -> None:
        if books is None:
            self._books: list = []
        else:
            self._books = books


    def __len__(self) -> int: # длина коллекции
        return len(self._books)
    

    def __getitem__(self, index: int | slice): # доступ по индексу или срезу
        if isinstance(index, int):
            if 0 <= index < len(self._books):
                return self._books[index]
            else:
                raise IndexError("Error: выход за пределы, индекс превышает длину")
        elif isinstance(index, slice):
            return BookCollection(self._books[index])
        else:
            raise TypeError("Error: не совпадение типа объекта для индекса (должно быть целое число или срез)")
    
        
    def __iter__(self) -> Iterator[Book]: # последовательный перебор книг
        return iter(self._books)
    

    def __repr__(self) -> str:
        return f"Коллекция книг: {self._books}"
    
    
    def __str__(self) -> str:
        return f"Коллекция книг: {self._books}"
    
    
    def __contains__(self, book: Book) -> bool: # проверка наличия книги в коллекции
        return book in self._books
    
    
    def __setitem__(self, index: int, book: Book) -> None: # установка книги по индексу
        self._books[index] = book

        
    def add_to_collection(self, book: Book) -> None: # добавление книги в коллекцию
        self._books.append(book)


    def remove_from_collection(self, book: Book) -> None: # удаление книги из коллекции
        if book not in self._books:
            raise ValueError('Error: попытка удалить несуществующий элемент')
        self._books.remove(book)


    def clear(self) -> None: # очистка коллекции
        self._books = []


    def is_empty(self) -> bool: # проверка на пустоту коллекции
        return (len(self._books) == 0)
    

class IndexDict: # словарь с индексами для быстрого поиска книг
    def __init__(self) -> None:
        self._by_isbn: Dict[str, Book] = {}
        self._by_author: Dict[str, BookCollection] = {}
        self._by_year: Dict[int, BookCollection] = {}
        self._by_genre: Dict[str, BookCollection] = {}


    def add_book(self, key: str, book: Book) -> None: # добавление книги в индексы
        if not isinstance(book, Book):
            raise TypeError("Error: значение не совпадает с нужным типом объекта - Book")

        if key in self._by_isbn:
            raise ExistError("Error: данная книга уже существует. Для обновления информации используйте другую комнаду")
        
        # добавляем в основной индекс
        self._by_isbn[key] = book
        
        # добавляем в индекс по автору
        if book.author not in self._by_author:
            self._by_author[book.author] = BookCollection()
        self._by_author[book.author].add_to_collection(book)
        
        # добавляем в индекс по году
        if book.year not in self._by_year:
            self._by_year[book.year] = BookCollection()
        self._by_year[book.year].add_to_collection(book)
        
        # добавляем в индекс по жанру
        if book.genre not in self._by_genre:
            self._by_genre[book.genre] = BookCollection()
        self._by_genre[book.genre].add_to_collection(book)


    def remove_book(self, key: str) -> None: # удаление книги из индексов
        if key not in self._by_isbn:
            raise KeyError(f"Error: книга с ISBN '{key}' не найдена")
        
        book = self._by_isbn[key]

        # удаляем из индекса по автору
        if book.author in self._by_author:
            self._by_author[book.author].remove_from_collection(book)
            if not self._by_author[book.author]:
                del self._by_author[book.author]
        
        # удаляем из индекса по году
        if book.year in self._by_year:
            self._by_year[book.year].remove_from_collection(book)
            if not self._by_year[book.year]:
                del self._by_year[book.year]
        
        # удаляем из индекса по жанру
        if book.genre in self._by_genre:
            self._by_genre[book.genre].remove_from_collection(book)
            if not self._by_genre[book.genre]:
                del self._by_genre[book.genre]
        
        del self._by_isbn[key] # удаляем из основного индекса


    def update_book(self, isbn: str, **kwargs) -> None: # обновление информации о книге
        # используем kwargs для всех возможных параметров книги,
        # чтобы не проверять каждый отдельно

        if isbn not in self._by_isbn:
            raise KeyError(f"Error: книга с ISBN '{isbn}' не найдена")
        
        book = self._by_isbn[isbn]
        old_author = book.author
        old_year = book.year
        old_genre = book.genre
        
        # обновляем атрибуты книги
        for key, value in kwargs.items():
            if hasattr(book, key):
                setattr(book, key, value)
        
        # если изменился автор, обновляем индекс
        if 'author' in kwargs and kwargs['author'] != old_author:
            if old_author in self._by_author:
                self._by_author[old_author].remove_from_collection(book)
                if self._by_author[old_author].is_empty():
                    del self._by_author[old_author]
            
            if book.author not in self._by_author:
                self._by_author[book.author] = BookCollection()
            self._by_author[book.author].add_to_collection(book)
        
        # если изменился год, обновляем индекс
        if 'year' in kwargs and kwargs['year'] != old_year:
            if old_year in self._by_year:
                self._by_year[old_year].remove_from_collection(book)
                if self._by_year[old_year].is_empty():
                    del self._by_year[old_year]
            
            if book.year not in self._by_year:
                self._by_year[book.year] = BookCollection()
            self._by_year[book.year].add_to_collection(book)
        
        # если изменился жанр, обновляем индекс
        if 'genre' in kwargs and kwargs['genre'] != old_genre:
            if old_genre in self._by_genre:
                self._by_genre[old_genre].remove_from_collection(book)
                if self._by_genre[old_genre].is_empty():
                    del self._by_genre[old_genre]
            
            if book.genre not in self._by_genre:
                self._by_genre[book.genre] = BookCollection()
            self._by_genre[book.genre].add_to_collection(book)


    def get_by_isbn(self, isbn: str): # поиск книги по ISBN
        try:
            return self._by_isbn.get(isbn)
        
        except KeyError:
            print(f"Error: неверный isbn - '{isbn}'")
    

    def get_by_author(self, author: str):  # поиск книг по автору
        try:
            book_collection = self._by_author[author]
            books = list(book_collection)
            print(f"Поиск по автору '{author}': найдено {len(books)} книг(и)")
            return books
        
        except KeyError:
            print(f"Автор '{author}' не найден в каталоге")
            return []


    def get_by_year(self, year: int):  # поиск книг по году
        try:
            book_collection = self._by_year[year]
            books = list(book_collection)
            print(f"Поиск по году {year}: найдено {len(books)} книг(и)")
            return books
        
        except KeyError:
            print(f"Книги {year} года не найдены в каталоге")
            return []
    
    
    def get_by_genre(self, genre: str):  # поиск книг по жанру
        try:
            book_collection = self._by_genre[genre]
            books = list(book_collection)
            print(f"Поиск по жанру '{genre}': найдено {len(books)} книг(и)")
            return books
        
        except KeyError:
            print(f"Книги жанра '{genre}' не найдены в каталоге")
            return []


class Library: # класс библиотеки
    def __init__(self):
        self._books = BookCollection() # коллекция книг в библиотеке
        self._index = IndexDict() # индексы для быстрого поиска книг


    def add_book_to_lib(self, book: Book) -> None: # добавить книгу в библиотеку
        self._books.add_to_collection(book)
        self._index.add_book(book.isbn, book)

    
    def remove_book_from_lib(self, isbn: str) -> None: # удалить книгу из библиотеки
        book = self._index.get_by_isbn(isbn)
        if book is None:
            raise KeyError(f"Error: книга с ISBN '{isbn}' не найдена в библиотеке")
        self._books.remove_from_collection(book)
        self._index.remove_book(isbn)


    def update_book_info(self, isbn: str, **kwargs) -> None: # обновить информацию о книге
        self._index.update_book(isbn, **kwargs)

    
    def find_by_author(self, author: str) -> BookCollection: # поиск по автору
        return self._index.get_by_author(author)
    

    def find_by_year(self, year: str) -> BookCollection: # поиск по году
        return self._index.get_by_year(year)
    

    def find_by_genre(self, genre: str) -> BookCollection: # поиск по жанру
        return self._index.get_by_genre(genre)
    

    def find_by_isbn(self, isbn: str) -> Book: # поиск по isbn
        return self._index.get_by_isbn(isbn)
    

    def __len__(self) -> int: # количество книг в библиотеке
        return len(self._books)
    

    def __contains__(self, book: Book) -> bool: # проверка наличия книги в библиотеке
        return book in self._books
    

    def __iter__(self) -> Iterator[Book]:
        return iter(self._books)

