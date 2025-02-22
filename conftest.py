import pytest
from books_collector import BooksCollector

@pytest.fixture
def collector():
    return BooksCollector()

@pytest.fixture
def add_book(collector):
    return collector.add_new_book

@pytest.fixture
def add_genre(collector):
    return collector.set_book_genre

@pytest.fixture
def add_to_favorites(collector):
    return collector.add_book_in_favorites

@pytest.fixture
def delete_from_favorites(collector):
    return collector.delete_book_from_favorites
