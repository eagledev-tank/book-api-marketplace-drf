from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Book


class BookTestCase(APITestCase):
    def setUp(self):
        self.book_data = {
            'title': 'Test Book',
            'author': 'Author Name',
            'price': 9.99,
            'description': 'Test Book Description.',
            'stock': 22,
            'publication_date': '2024-09-11',
        }
        self.book = Book.objects.create(**self.book_data)

        def test_create_book(self):
            url = reverse('book-list')
            response = self.client.post(url, data=self.book_data, format='json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertEqual(Book.objects.count(), 2)
            self.assertEqual(Book.objects.get(id=response.data['id']).title, 'Test Book')

        def test_get_book(self):
            url = reverse('book-detail', args=[self.book.id])
            response = self.client.get(url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data['title'], self.book.title)

        def test_update_book(self):
            url = reverse('book-detail', args=[self.book.id])
            updated_data = {'title': 'Test Book Updated'}
            response = self.client.put(url, data=updated_data, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.book.refresh_from_db()
            self.assertEqual(self.book.title, 'Test Book Updated')

        def test_delete_book(self):
            url = reverse('book-detail', args=[self.book.id])
            response = self.client.delete(url)
            self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
            self.assertEqual(Book.objects.count(), 0)
