from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class User(AbstractUser):
	# Extend as needed (e.g., add role field if required)
	pass

class Book(models.Model):
	title = models.CharField(max_length=255)
	author = models.CharField(max_length=255)
	isbn = models.CharField(max_length=13, unique=True)
	page_count = models.PositiveIntegerField()
	available = models.BooleanField(default=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return f"{self.title} by {self.author}"

class Loan(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	book = models.ForeignKey(Book, on_delete=models.CASCADE)
	borrowed_at = models.DateTimeField(auto_now_add=True)
	returned_at = models.DateTimeField(null=True, blank=True)

	def __str__(self):
		return f"{self.user.username} borrowed {self.book.title}"
