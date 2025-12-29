from rest_framework.views import APIView
from rest_framework import status, permissions, filters
from rest_framework.response import Response
from .models import Book, Borrow, User
from .serializers import BookSerializer, BorrowSerializer, UserSerializer, RegisterSerializer
from .permissions import IsAdminOrReadOnly, IsOwnerOrAdmin
from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class RegisterView(APIView):
	permission_classes = (permissions.AllowAny,)

	@swagger_auto_schema(request_body=RegisterSerializer, responses={201: UserSerializer})
	def post(self, request):
		serializer = RegisterSerializer(data=request.data)
		if serializer.is_valid():
			user = serializer.save()
			return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BookListCreateAPIView(APIView):
	permission_classes = [IsAdminOrReadOnly]

	@swagger_auto_schema(responses={200: BookSerializer(many=True)})
	def get(self, request):
		search = request.GET.get('search', '')
		books = Book.objects.all()
		if search:
			books = books.filter(title__icontains=search) | books.filter(author__icontains=search) | books.filter(isbn__icontains=search)
		serializer = BookSerializer(books, many=True)
		return Response(serializer.data)

	@swagger_auto_schema(request_body=BookSerializer, responses={201: BookSerializer})
	def post(self, request):
		serializer = BookSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BookRetrieveUpdateDestroyAPIView(APIView):
	permission_classes = [IsAdminOrReadOnly]

	@swagger_auto_schema(responses={200: BookSerializer})
	def get(self, request, pk):
		try:
			book = Book.objects.get(pk=pk)
		except Book.DoesNotExist:
			return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
		serializer = BookSerializer(book)
		return Response(serializer.data)

	@swagger_auto_schema(request_body=BookSerializer, responses={200: BookSerializer})
	def put(self, request, pk):
		try:
			book = Book.objects.get(pk=pk)
		except Book.DoesNotExist:
			return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
		serializer = BookSerializer(book, data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	@swagger_auto_schema(responses={204: 'No Content'})
	def delete(self, request, pk):
		try:
			book = Book.objects.get(pk=pk)
		except Book.DoesNotExist:
			return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
		book.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)

class BorrowListCreateAPIView(APIView):
	permission_classes = [permissions.IsAuthenticated]

	@swagger_auto_schema(responses={200: BorrowSerializer(many=True)})
	def get(self, request):
		Borrows = Borrow.objects.filter(user=request.user)
		serializer = BorrowSerializer(Borrows, many=True)
		return Response(serializer.data)

	@swagger_auto_schema(request_body=BorrowSerializer, responses={201: BorrowSerializer})
	def post(self, request):
		serializer = BorrowSerializer(data=request.data)
		if serializer.is_valid():
			book = serializer.validated_data['book']
			if not book.available:
				return Response({'book': 'Book is not available.'}, status=status.HTTP_400_BAD_REQUEST)
			book.available = False
			book.save()
			serializer.save(user=request.user)
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BorrowReturnAPIView(APIView):
	permission_classes = [permissions.IsAuthenticated]

	@swagger_auto_schema(responses={200: BorrowSerializer})
	def post(self, request, pk):
		try:
			Borrow = Borrow.objects.get(pk=pk, user=request.user)
		except Borrow.DoesNotExist:
			return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
		if Borrow.returned_at:
			return Response({'detail': 'Book already returned.'}, status=status.HTTP_400_BAD_REQUEST)
		Borrow.returned_at = timezone.now()
		Borrow.book.available = True
		Borrow.book.save()
		Borrow.save()
		return Response(BorrowSerializer(Borrow).data)

class UserListAPIView(APIView):
	permission_classes = [permissions.IsAdminUser]

	@swagger_auto_schema(responses={200: UserSerializer(many=True)})
	def get(self, request):
		users = User.objects.all()
		serializer = UserSerializer(users, many=True)
		return Response(serializer.data)
