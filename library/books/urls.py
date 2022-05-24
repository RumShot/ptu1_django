from django.urls import include, path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('authors/', views.authors, name='authors'),
    path('author/<int:author_id>/', views.author, name='author'),
    path('books/', views.BookListView.as_view(), name='books'),
    path('books/<int:pk>/', views.BookDetailView.as_view(), name='book'),
    path('my_books/', views.LoanedBooksByUser.as_view(), name='my_books'),
    # path('search/', views.search, name='search'),
]