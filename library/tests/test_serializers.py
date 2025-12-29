import pytest
from library.models import Book, User, Borrow
from library.serializers import BookSerializer, UserSerializer, BorrowSerializer

@pytest.mark.django_db
def test_book_serializer():
    book = Book.objects.create(title="SerTest", author="SerAuthor", isbn="1234567890999", page_count=123)
    serializer = BookSerializer(book)
    data = serializer.data
    assert data["title"] == "SerTest"
    assert data["author"] == "SerAuthor"
    assert data["isbn"] == "1234567890999"

@pytest.mark.django_db
def test_user_serializer():
    user = User.objects.create_user(username="seruser", password="pass", email="seruser@example.com")
    serializer = UserSerializer(user)
    data = serializer.data
    assert data["username"] == "seruser"
    assert data["email"] == "seruser@example.com"

@pytest.mark.django_db
def test_loan_serializer():
    user = User.objects.create_user(username="serloan", password="pass")
    book = Book.objects.create(title="SerLoanBook", author="SerLoanAuthor", isbn="1234567890888", page_count=111)
    loan = Borrow.objects.create(user=user, book=book)
    serializer = BorrowSerializer(loan)
    data = serializer.data
    assert data["user"]["username"] == "serloan"
    assert data["book"]["title"] == "SerLoanBook"
