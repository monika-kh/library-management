import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from library.models import Book, User, Borrow

@pytest.mark.django_db
def test_register_view():
    client = APIClient()
    url = reverse('register')
    data = {
        "username": "viewuser",
        "email": "viewuser@example.com",
        "password": "StrongPass123!",
        "password2": "StrongPass123!"
    }
    response = client.post(url, data)
    assert response.status_code == 201
    assert response.data["username"] == "viewuser"

@pytest.mark.django_db
def test_book_list_create_view():
    client = APIClient()
    admin = User.objects.create_superuser(username="admin", password="adminpass")
    client.force_authenticate(user=admin)
    url = reverse('book-list-create')
    data = {"title": "ViewBook", "author": "ViewAuthor", "isbn": "1234567890777", "page_count": 222}
    response = client.post(url, data)
    assert response.status_code == 201
    assert response.data["title"] == "ViewBook"
    response = client.get(url)
    assert response.status_code == 200
    assert any(book["title"] == "ViewBook" for book in response.data)

@pytest.mark.django_db
def test_loan_create_and_return_view():
    client = APIClient()
    user = User.objects.create_user(username="loanuser", password="pass")
    book = Book.objects.create(title="LoanBook", author="LoanAuthor", isbn="1234567890666", page_count=333)
    client.force_authenticate(user=user)
    loan_url = reverse('borrow-list-create')
    data = {"book_id": book.id}
    response = client.post(loan_url, data)
    assert response.status_code == 201
    loan_id = response.data["id"]
    return_url = reverse('borrow-return', args=[loan_id])
    response = client.post(return_url)
    assert response.status_code == 200
    assert response.data["returned_at"] is not None
