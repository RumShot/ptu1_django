from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views import generic
from .models import Book, Author, Bookinstance, Genre


# gali buti 2 view funkciniai ir ... 
# Funkcinis view
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


def authors(request):
    authors = Author.objects.all()
    return render(request, 'books/authors.html', {'authors': authors})


def author(request, author_id):
    author = get_object_or_404(Author, pk=author_id)
    return render(request, 'books/author.html', {'author': author})


# class based views
class BookListView(generic.ListView):
    model = Book
    context_object_name = 'books'
    # queryset = Book.objects.filter(title__icontains='')
    template_name = 'books/book_list.html'
    extra_context = {'spalva2': '#06f'}

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request and self.request.GET.get('search_title'):
            queryset = queryset.filter(title__icontains=self.request.GET.get('search_title'))
        return queryset

    #  2 skirtingi aprasymo budai, rezultatas tas pats
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'spalva': '#fc0'})
        # context = {}
        # context.update({'books': self.get_queryset()})
        return context


class BookDetailView(generic.DeleteView):
    model = Book
    template_name = 'books/book_detail.html'