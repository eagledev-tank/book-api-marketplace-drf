# import pytest
# from rest_framework.test import APIClient
# from book.models import Book
#
#
# @pytest.mark.django_db
# def test_book_integration():
#     client = APIClient()
#
#     # Yangi kitob yaratish
#     response = client.post('/api/v1/book/', {
#         'title': 'Integration Test Book',
#         'author': 'Author',
#         'price': 100
#     })
#
#     assert response.status_code == 201
#
#     book_id = response.data['id']
#     response = client.get(f'/api/v1/book/{book_id}/')
#
#     assert response.status_code == 200
#     assert response.data['title'] == 'Integration Test Book'
