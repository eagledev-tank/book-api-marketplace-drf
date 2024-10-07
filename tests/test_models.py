# import pytest
# from book.models import Book
#
#
# @pytest.mark.django_db
# def test_create_book():
#     book = Book.objects.create(title="Test Book", author="Test Author",
#                                description="Test Description", price="100",
#                                stock=300, publication_date="2024-09-30")
#
#     assert book.title == "Test Book"
#     assert book.author == "Test Author"
#     assert book.description == "Test Description"
#     assert book.price == "100"
#     assert book.stock == 300
#     assert book.publication_date == "2024-09-30"
