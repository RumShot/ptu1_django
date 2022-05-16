from django.contrib import admin
from .models import Author, Book, Bookinstance, Genre


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name' ,'get_books_count')
    list_display_links = ('first_name', )


# display list columns in admin panel
class BookInstanceInline(admin.TabularInline):
    model = Bookinstance
    can_delete = False
    extra = 0 


class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genres')
    list_filter = ('author', 'genre')
    # list_display = ('__str__', 'title', 'author', 'display_genres')
    inlines = (BookInstanceInline, )


class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book', 'status', 'due_back', 'id')
    list_filter = ('status', 'due_back')
    search_fields = ('id', 'book__title')
    readonly_fields = ('id', )
    list_editable = ('status', 'due_back')

    fieldsets = (
        ('pagrindine informacija', {'fields': ('id', 'book')}),
        ('prieinamumas', {'fields': ('status', 'due_back')})
    )


admin.site.register(Author, AuthorAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Bookinstance, BookInstanceAdmin)
admin.site.register(Genre)
