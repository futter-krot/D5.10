from django.contrib import admin

from p_library.models import Author, Book, Publisher


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author")
    fields = (
        "ISBN",
        "title",
        "description",
        "year_release",
        "author",
        "price",
        "copy_count",
        "publisher",
    )


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    pass


@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    pass
