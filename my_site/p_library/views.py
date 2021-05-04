from django.core import serializers
from django.forms import modelform_factory
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.template import loader
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from p_library.forms import (AuthorCreateForm, BookCreateFormMin, BookSendForm,
                             FriendCreateForm, PublisherCreateForm)
from p_library.models import Author, Book, BookReader, Friend, Publisher

# Create your views here.


def books_json(request):
    books = Book.objects.all()
    qs_json = serializers.serialize("json", books)
    return HttpResponse(qs_json, content_type="application/json")

@login_required
def books_list(request):
    template = loader.get_template("index.html")
    books = Book.objects.all()
    biblio_data = {
        "title": "мою библиотеку",
        "books": books,
        "loop": range(1, 101),
    }
    return HttpResponse(template.render(biblio_data, request))


@login_required
def book_increment(request):
    if request.method == "POST":
        book_id = request.POST["id"]
        if not book_id:
            return redirect("p_library:books")
        else:
            book = Book.objects.filter(id=book_id).first()
            if not book:
                return redirect("p_library:books")
            book.copy_count += 1
            book.save()
        return redirect("p_library:books")
    else:
        return redirect("p_library:books")


@login_required
def book_decrement(request):
    if request.method == "POST":
        book_id = request.POST["id"]
        if not book_id:
            return redirect("p_library:books")
        else:
            book = Book.objects.filter(id=book_id).first()
            if not book:
                return redirect("p_library:books")
            if book.copy_count < 1:
                book.copy_count = 0
            else:
                book.copy_count -= 1
            book.save()
        return redirect("p_library:books")
    else:
        return redirect("p_library:books")


class AuthorAdd(LoginRequiredMixin, CreateView):
    model = Author
    form_class = AuthorCreateForm
    success_url = reverse_lazy("p_library:create")
    template_name = "item_add.html"



class AuthorList(LoginRequiredMixin, ListView):
    model = Author
    template_name = "authors.html"


class AuthorDetail(LoginRequiredMixin, DetailView):
    model = Author
    template_name = "author_detail.html"


class PublisherAdd(LoginRequiredMixin, CreateView):
    model = Publisher
    form_class = PublisherCreateForm
    success_url = reverse_lazy("p_library:create")
    template_name = "item_add.html"

@login_required
def publisher_list(request):
    return render(
        request,
        "publishers.html",
        {
            "publishers": Book.objects.select_related("publisher").order_by(
                "publisher"
            ),
        },
    )


class PublisherDetail(LoginRequiredMixin, DetailView):
    model = Publisher
    template_name = "publisher_detail.html"


class FriendAdd(LoginRequiredMixin, CreateView):
    model = Friend
    form_class = FriendCreateForm
    success_url = reverse_lazy("p_library:friend_list")
    template_name = "item_add.html"


class FriendList(LoginRequiredMixin, ListView):  # pylint: disable=too-many-ancestors
    model = Friend
    template_name = "friends.html"


class FriendDetail(LoginRequiredMixin, DetailView):
    model = Friend
    template_name = "friend_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["sent_books"] = self.object.bookreader_set.all()
        return context


class BookDetail(LoginRequiredMixin, DetailView):
    model = Book
    template_name = "book_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["author"] = self.object.author
        context["publisher"] = self.object.publisher
        return context


class BookSend(LoginRequiredMixin, CreateView):
    model = BookReader
    form_class = BookSendForm
    success_url = reverse_lazy("p_library:friend_list")
    template_name = "book_send.html"

@login_required
def create_book_full(request):
    BookForm = modelform_factory(Book, exclude=("author", "publisher", "book_reader"))
    if request.method == "POST":
        book_form = BookForm(request.POST, request.FILES)
        author_form = AuthorCreateForm(request.POST, request.FILES)
        publisher_form = PublisherCreateForm(request.POST, request.FILES)
        if (
            book_form.is_valid()
            and author_form.is_valid()
            and publisher_form.is_valid()
        ):
            book = book_form.save(commit=False)
            author = author_form.save()
            publisher = publisher_form.save()
            book.author = author
            book.publisher = publisher
            book.save()
            return redirect(book)
    else:
        book_form = BookForm()
        author_form = AuthorCreateForm()
        publisher_form = PublisherCreateForm()

    return render(
        request,
        "book_add_full.html",
        {
            "author": author_form,
            "publisher": publisher_form,
            "book": book_form,
        },
    )

@login_required
def create_redirect(request):
    if request.GET.get('form'):
        return redirect('p_library:create_min')
    return redirect('p_library:create_full')



class BookCreateMin(LoginRequiredMixin, CreateView):
    model = Book
    form_class = BookCreateFormMin
    template_name = "book_add.html"

    def form_valid(self, form):
        self.object = form.save(commit=False) # pylint: disable=attribute-defined-outside-init
        print(form["author"])
        print(type(form["author"]))
        self.object.author = form.cleaned_data["author"]
        self.object.publisher = form.cleaned_data["publisher"]
        self.object.save()
        print(self.get_success_url())
        return HttpResponseRedirect(self.get_success_url())
