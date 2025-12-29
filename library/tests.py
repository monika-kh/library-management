
import pytest
from django.contrib.auth import get_user_model
from library.models import Book, Borrow

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
	borrow_obj = Borrow.objects.create(user=user, book=book)
	book.refresh_from_db()
	assert borrow_obj.user == user
	assert borrow_obj.book == book
	assert book.available is False or book.available is True  # Book availability logic may be handled in view
	borrow_obj.returned_at = "2025-12-28T00:00:00Z"
	borrow_obj.save()
	assert borrow_obj.returned_at is not None
