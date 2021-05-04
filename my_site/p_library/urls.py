from django.urls import path

from p_library import views

app_name = "p_library"

urlpatterns = [
    path("", views.books_list, name="books"),
    path("books", views.books_list, name="books"),
    path("books/json", views.books_json),
    path("books/send", views.BookSend.as_view(), name="book_send"),
    path("books/create/", views.create_redirect, name="create"),
    path("books/create/full", views.create_book_full, name="create_full"),
    path("books/create/min", views.BookCreateMin.as_view(), name="create_min"),
    path("books/<int:pk>", views.BookDetail.as_view(), name="book_detail"),
    path("publishers", views.publisher_list, name="publishers"),
    path(
        "publishers/<int:pk>", views.PublisherDetail.as_view(), name="publisher_detail"
    ),
    path("friend/create", views.FriendAdd.as_view(), name="friend_create"),
    path("friends/<int:pk>", views.FriendDetail.as_view(), name="friend_detail"),
    path("friends", views.FriendList.as_view(), name="friend_list"),
    path("authors", views.AuthorList.as_view(), name="author_list"),
    path("authors/<int:pk>", views.AuthorDetail.as_view(), name="author_detail"),
]
