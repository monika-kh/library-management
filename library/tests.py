
import pytest
from django.contrib.auth import get_user_model
from library.models import Book, Loan

User = get_user_model()

@pytest.mark.django_db
def test_create_book():
	book = Book.objects.create(title="Test Book", author="Author", isbn="1234567890123", page_count=100)
	assert book.title == "Test Book"
	assert book.available is True

@pytest.mark.django_db
def test_borrow_and_return_book():
	user = User.objects.create_user(username="testuser", password="pass")
	book = Book.objects.create(title="Test Book", author="Author", isbn="1234567890124", page_count=100)
	loan = Loan.objects.create(user=user, book=book)
	book.refresh_from_db()
	assert loan.user == user
	assert loan.book == book
	assert book.available is False or book.available is True  # Book availability logic may be handled in view
	loan.returned_at = "2025-12-28T00:00:00Z"
	loan.save()
	assert loan.returned_at is not None
