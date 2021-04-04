from django.test import TestCase, Client
from django.shortcuts import reverse

from .models import Book

# Create your tests here.

class BookTests(TestCase):
    def setUp(self):
        self.book = Book.objects.create(
            title = 'Harry Potter',
            author = 'JK Rowling',
            price = 25.99,
        )

    def test_book_listing(self):
        '''
        Tests that both its string representation and content
        are correct.
        '''
        self.assertEqual(f'{self.book.title}', 'Harry Potter')
        self.assertEqual(f'{self.book.author}', 'JK Rowling')
        self.assertEqual(f'{self.book.price}', '25.99')

    def test_book_list_view(self):
        response = self.client.get(reverse('book_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Harry Potter')
        self.assertTemplateUsed(response, 'books/book_list.html')
    
    def test_book_detail_view(self):
        response = self.client.get(self.book.get_absolute_url())
        no_response = self.client.get('/books/12345/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, 'Harry Potter')
        self.assertTemplateUsed(response, 'books/book_detail.html')
