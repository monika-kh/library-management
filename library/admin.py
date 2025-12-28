from django.contrib import admin


# Register your models here.
from .models import Book, Loan
from django.contrib import admin

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
	list_display = ("title", "author", "isbn", "page_count", "available")
	search_fields = ("title", "author", "isbn")

@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
	list_display = ("user", "book", "borrowed_at", "returned_at")
	search_fields = ("user__username", "book__title")
