from django.contrib import admin
from django import forms

from . import models


class NickAdminForm(forms.ModelForm):

    class Meta:
        model = models.Nick
        fields = "__all__"


class NickAdmin(admin.ModelAdmin):
    form = NickAdminForm
    list_display = [
        "name",
        "gender",
    ]
    readonly_fields = [
        "name",
        "gender",
    ]


class CategoryAdminForm(forms.ModelForm):

    class Meta:
        model = models.Category
        fields = "__all__"


class CategoryAdmin(admin.ModelAdmin):
    form = CategoryAdminForm
    list_display = [
        "slug",
        "name",
    ]
    readonly_fields = [
        "slug",
        "name",
    ]


class PostAdminForm(forms.ModelForm):

    class Meta:
        model = models.Post
        fields = "__all__"


class PostAdmin(admin.ModelAdmin):
    form = PostAdminForm
    list_display = [
        "reply_to",
        "bytes",
        "url",
        "votes",
        "hits",
        "post_date",
        "title",
    ]
    readonly_fields = [
        "reply_to",
        "bytes",
        "url",
        "votes",
        "hits",
        "post_date",
        "title",
    ]


admin.site.register(models.Nick, NickAdmin)
admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.Post, PostAdmin)
