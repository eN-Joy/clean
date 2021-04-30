from django import forms
from . import models


class NickForm(forms.ModelForm):
    class Meta:
        model = models.Nick
        fields = [
            "name",
            "gender",
        ]


class CategoryForm(forms.ModelForm):
    class Meta:
        model = models.Category
        fields = [
            "slug",
            "name",
        ]


class PostForm(forms.ModelForm):
    class Meta:
        model = models.Post
        fields = [
            "reply_to",
            "bytes",
            "url",
            "votes",
            "hits",
            "post_date",
            "title",
            "nick",
            "category",
        ]
