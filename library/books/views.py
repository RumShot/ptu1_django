from django.shortcuts import render
from django.http import HttpResponse
from .models import Book, Author, Bookinstance, Genre


# Create your views here.
def index(request):
    num_books = Book.objects.all().count()
    num_instances = Bookinstance.objects.all().count()
    num_instances_available = Bookinstance.objects.filter(status__exact='g').count()
    num_authors = Author.objects.all().count()

    context = {
        'num_authors': num_authors,
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
    }

    return render(request, 'books/index.html', context)