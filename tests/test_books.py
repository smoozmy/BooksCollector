import pytest
from conftest import collector, add_book, add_genre, add_to_favorites, delete_from_favorites

class TestBooksCollector:

    def test_add_new_book_add_two_books(self, collector, add_book):
        add_book('Гордость и предубеждение и зомби')
        add_book('Что делать, если ваш кот хочет вас убить')

        assert len(collector.get_books_genre()) == 2

    def test_add_new_book_add_duplicate_book(self, collector, add_book):
        add_book('Как тестируют в Google')
        add_book('Как тестируют в Google')

        assert len(collector.get_books_genre()) == 1

    def test_add_new_book_incorrect_length(self, collector, add_book):
        add_book('')
        add_book('A' * 41)

        assert len(collector.get_books_genre()) == 0

    def test_set_book_genre_correct(self, collector, add_book, add_genre):
        add_book('Как тестируют в Google')
        add_genre('Как тестируют в Google', 'Фантастика')

        assert collector.get_book_genre('Как тестируют в Google') == 'Фантастика'

    def test_set_book_genre_incorrect(self, collector, add_book, add_genre):
        add_book('Как тестируют в Google')
        add_genre('Как тестируют в Google', 'Приключения')

        assert collector.get_book_genre('Как тестируют в Google') == ''

    @pytest.mark.parametrize("book_name, genre", [
        ("Как тестируют в Google", "Фантастика"),
        ("Оно", "Ужасы"),
    ])
    def test_get_books_with_specific_genre(self, collector, add_book, add_genre, book_name, genre):
        add_book(book_name)
        add_genre(book_name, genre)

        assert collector.get_books_with_specific_genre(genre) == [book_name]

    def test_get_books_with_specific_genre_empty(self, collector):
        assert collector.get_books_with_specific_genre('Фантастика') == []

    def test_get_books_for_children(self, collector, add_book, add_genre):
        add_book('Как тестируют в Google')
        add_genre('Как тестируют в Google', 'Фантастика')

        add_book('Оно')
        add_genre('Оно', 'Ужасы')

        assert collector.get_books_for_children() == ['Как тестируют в Google']

    def test_add_book_in_favorites(self, collector, add_book, add_to_favorites):
        add_book('Как тестируют в Google')
        add_to_favorites('Как тестируют в Google')

        assert 'Как тестируют в Google' in collector.get_list_of_favorites_books()

    def test_add_book_in_favorites_duplicate(self, collector, add_book, add_to_favorites):
        add_book('Как тестируют в Google')
        add_to_favorites('Как тестируют в Google')
        add_to_favorites('Как тестируют в Google')

        assert len(collector.get_list_of_favorites_books()) == 1

    def test_add_book_in_favorites_nonexistent(self, collector, add_to_favorites):
        add_to_favorites('Несуществующая книга')

        assert len(collector.get_list_of_favorites_books()) == 0

    @pytest.mark.parametrize("book_name, initial_favorites, expected_favorites", [
        ("Как тестируют в Google", ["Как тестируют в Google"], []),
        ("Оно", [], []),
    ])
    def test_delete_book_from_favorites(self, collector, add_book, add_to_favorites, delete_from_favorites, book_name, initial_favorites, expected_favorites):
        add_book(book_name)
        for book in initial_favorites:
            add_to_favorites(book)
        delete_from_favorites(book_name)
        assert collector.get_list_of_favorites_books() == expected_favorites

    def test_get_list_of_favorites_books_empty(self, collector):
        assert collector.get_list_of_favorites_books() == []
