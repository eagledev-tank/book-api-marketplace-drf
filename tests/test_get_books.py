# import pytest
# from rest_framework import status
# from rest_framework.test import APIClient
# from book.models import Book
# from django.urls import reverse
#
#
# @pytest.mark.django_db
# def test_get_books():
#     # Book.objects.create(title="Test Book", author="Test Author")
#     client = APIClient()
#     url = reverse('book-list')
#     response = client.get(url)
#
#     assert response.status_code == status.HTTP_200_OK
#     assert len(response.data) > 0
