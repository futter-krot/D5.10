from crispy_forms.helper import FormHelper
from django import forms
from django.forms import ModelChoiceField

from p_library.models import Author, Book, BookReader, Friend, Publisher


class PublisherChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return str(obj.name)


class AuthorChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return str(obj.full_name)

class BookChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return str(obj.title)

class FriendChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return str(obj.name)

class FriendCreateForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput)

    class Meta:
        model = Friend
        fields = "__all__"


class BookSendForm(forms.ModelForm):
    book = BookChoiceField(queryset=Book.objects.all())
    friend = FriendChoiceField(queryset=Friend.objects.all())

    class Meta:
        model = BookReader
        fields = "__all__"


class AuthorCreateForm(forms.ModelForm):
    full_name = forms.CharField(widget=forms.TextInput)

    class Meta:
        model = Author
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = "id-Author"
        self.helper.form_class = "blueForms"


class BookCreateForm(forms.ModelForm):
    class Meta:
        model = Book
        exclude = [
            "author",
            "publisher",
            "book_reader",
        ]


class PublisherCreateForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput)

    class Meta:
        model = Publisher
        fields = "__all__"


class BookCreateFormMin(BookCreateForm):
    author = AuthorChoiceField(queryset=Author.objects.all())
    publisher = PublisherChoiceField(queryset=Publisher.objects.all())
