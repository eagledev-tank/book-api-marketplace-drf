# import pytest
# from book.serializers import BookSerializer
# from book.models import Book
#
#
# @pytest.mark.django_db
# def test_book_serializer():
#     book = Book.objects.create(title="Test Book", author="Test Author",
#                                price="100", stock=100, publication_date="2024-09-30",
#                                description="Test Description")
#     serializer = BookSerializer(book)
#     assert serializer.data == ['title'] == "Test Book"
#     assert serializer.data == ['author'] == "Test Author"
#     assert serializer.data == ['price'] == "100"
#     assert serializer.data == ['stock'] == "100"
#     assert serializer.data == ['publication_date'] == "2024-09-30"
#     assert serializer.data == ['description'] == "Test Description"
