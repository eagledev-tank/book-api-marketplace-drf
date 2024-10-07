# import pytest
# from rest_framework.test import APIClient
# from book.models import Book
#
#
# @pytest.mark.django_db
# def test_get_books():
#     Book.objects.create(title="Test Book", author="Test Author",
#                         price="100", stock=100, publication_date="2024-09-30",
#                         description="Test Description")
#     Book.objects.create(title="Test Book", author="Test Author1",
#                         price="100", stock=100, publication_date="2024-09-30",
#                         description="Test Description")
#     client = APIClient()
#     response = client.get('http://127.0.0.1:8000/api/v1/Book/')
#     assert response.status_code == 200
#     assert len(response.data) == 2
