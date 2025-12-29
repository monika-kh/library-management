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
def test_loan_creation_and_return():
    user = User.objects.create_user(username="testuser", password="pass")
    book = Book.objects.create(title="Test Book", author="Author", isbn="1234567890124", page_count=100)
    loan = Loan.objects.create(user=user, book=book)
    assert loan.user == user
    assert loan.book == book
    assert loan.returned_at is None
    loan.returned_at = "2025-12-29T00:00:00Z"
    loan.save()
    assert loan.returned_at is not None
