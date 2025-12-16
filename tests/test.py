from src.library_classes import Book, BookCollection, IndexDict, Library


def test_empty_coll_init():
    collection = BookCollection()
    assert len(collection) == 0
    assert collection.is_empty()


def test_collection_init_with_items():
    book_1 = Book("Война и мир", "Лев Толстой", 1869, "Роман", "978-5-123-45678-0")
    book_2 = Book("Преступление и наказание", "Фёдор Достоевский", 1866, "Роман", "978-5-234-56789-1")
    books = [book_1, book_2]
    collection = BookCollection(books)
    assert len(collection) == 2
    assert not collection.is_empty()


def test_collection_add_and_remove():
    collection = BookCollection()
    book = Book("Тест", "Автор", 2024, "Жанр", "978-5-000-00000-0")
    collection.add_to_collection(book)
    assert len(collection) == 1
    assert book in collection
    
    collection.remove_from_collection(book)
    assert len(collection) == 0
    assert book not in collection


def test_index_dict_add_book():
    index_dict = IndexDict()
    book = Book("Война и мир", "Лев Толстой", 1869, "Роман", "978-5-123-45678-0")
    index_dict.add_book(book.isbn, book)
    
    assert book.isbn in index_dict._by_isbn
    assert book.author in index_dict._by_author
    assert book.year in index_dict._by_year
    assert book.genre in index_dict._by_genre


def test_add_some_books_same_author():
    book_2 = Book("Преступление и наказание", "Фёдор Достоевский", 1866, "Роман", "978-5-234-56789-1")
    book_3 = Book("Братья Карамазовы", "Фёдор Достоевский", 1880, "Роман", "978-5-345-67890-2")
    
    index_dict = IndexDict()
    index_dict.add_book(book_2.isbn, book_2)
    index_dict.add_book(book_3.isbn, book_3)
    
    assert len(index_dict._by_author['Фёдор Достоевский']) == 2
    assert book_2 in index_dict._by_author['Фёдор Достоевский']
    assert book_3 in index_dict._by_author['Фёдор Достоевский']


def test_index_dict_search():
    index_dict = IndexDict()
    book_1 = Book("Война и мир", "Лев Толстой", 1869, "Роман", "978-5-123-45678-0")
    book_2 = Book("Анна Каренина", "Лев Толстой", 1877, "Роман", "978-5-234-56789-1")
    
    index_dict.add_book(book_1.isbn, book_1)
    index_dict.add_book(book_2.isbn, book_2)
    
    found = index_dict.get_by_isbn(book_1.isbn)
    assert found == book_1

    tolstoy_books = index_dict.get_by_author("Лев Толстой")
    assert len(tolstoy_books) == 2


def test_init():
    lib = Library()
    assert isinstance(lib._books, BookCollection)
    assert isinstance(lib._index, IndexDict)
    assert len(lib) == 0


def test_add_some_books():
    book_1 = Book("Война и мир", "Лев Толстой", 1869, "Роман", "978-5-123-45678-0")
    book_2 = Book("Преступление и наказание", "Фёдор Достоевский", 1866, "Роман", "978-5-234-56789-1")
    book_3 = Book("Братья Карамазовы", "Фёдор Достоевский", 1880, "Роман", "978-5-345-67890-2")
    
    lib = Library()
    lib.add_book_to_lib(book_1)
    lib.add_book_to_lib(book_2)
    lib.add_book_to_lib(book_3)

    assert len(lib) == 3
    assert all(book in lib for book in [book_1, book_2, book_3])


def test_library_search():
    lib = Library()
    book_1 = Book("Война и мир", "Лев Толстой", 1869, "Роман", "978-5-123-45678-0")
    book_2 = Book("Преступление и наказание", "Фёдор Достоевский", 1866, "Роман", "978-5-234-56789-1")
    
    lib.add_book_to_lib(book_1)
    lib.add_book_to_lib(book_2)
    
    found = lib.find_by_isbn(book_1.isbn)
    assert found == book_1
    
    tolstoy_books = lib.find_by_author("Лев Толстой")
    assert len(tolstoy_books) == 1
    
    books_1869 = lib.find_by_year(1869)
    assert len(books_1869) == 1


def test_library_remove_and_update():
    lib = Library()
    book = Book("Тест", "Автор", 2020, "Жанр", "978-5-000-00000-0")
    
    lib.add_book_to_lib(book)
    assert len(lib) == 1
    
    lib.update_book_info(book.isbn, year=2024)
    updated = lib.find_by_isbn(book.isbn)
    assert updated.year == 2024

    lib.remove_book_from_lib(book.isbn)
    assert len(lib) == 0
