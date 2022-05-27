from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, reverse
from django.views import generic
from django.views.decorators.csrf import csrf_protect
from django.views.generic.edit import FormMixin
from .forms import BookReviewForm
from .models import Book, Author, Bookinstance


# gali buti 2 view funkciniai ir ... 
# Funkcinis view
def index(request):
    num_books = Book.objects.all().count()
    num_instances = Bookinstance.objects.all().count()
    num_instances_available = Bookinstance.objects.filter(status__exact='g').count()
    num_authors = Author.objects.all().count()
    num_visits = request.session.get('num_visits', 1 )
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_authors': num_authors,
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_visits': num_visits,
    }
    return render(request, 'books/index.html', context)


# def search(request):
#     search = request.GET.get('search')
#     search_result = Book.objects.filter(

#     )
#     return render(request, 'books/search.html', {'books': search_result, 'search': search,})

def authors(request):
    paginator = Paginator(Author.objects.all(), 3)
    page_number = request.GET.get('page')
    authors = paginator.get_page(page_number)
    
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
    # paginate_by = 6

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request and self.request.GET and self.request.GET.get('search'):
            search = self.request.GET.get('search')
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(summary__icontains=search) |
                Q(author__last_name__istartswith=search)
            )
        return queryset

    #  2 skirtingi aprasymo budai, rezultatas tas pats
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'spalva': '#fc0'})
        # context = {}
        # context.update({'books': self.get_queryset()})
        return context


class BookDetailView(generic.DetailView, FormMixin):
    model = Book
    template_name = 'books/book_detail.html'
    form_class = BookReviewForm

    def get_success_url(self):
        return reverse('book', kwargs={'pk': self.object.id })

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.instance.book = self.object
        form.instance.reviewer = self.request.user
        form.save()
        return super().form_valid(form)


class LoanedBooksByUser(LoginRequiredMixin, generic.ListView):
    model = Bookinstance
    template_name = 'books/user_book_list.html'
    paginate_by = 10

    def get_queryset(self):
        return super().get_queryset().filter(reader=self.request.user).filter(Q(status__exact='b') | Q(status__exact='r')).order_by('-due_back')