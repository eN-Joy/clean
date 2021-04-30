from django.views import generic
from . import models
from . import forms

import logging
logger = logging.getLogger('django')


class NickListView(generic.ListView):
    model = models.Nick
    form_class = forms.NickForm

    paginate_by = 20


class NickCreateView(generic.CreateView):
    model = models.Nick
    form_class = forms.NickForm


class NickDetailView(generic.DetailView):
    model = models.Nick
    form_class = forms.NickForm

    template_name = 'nick/nick_detail_v1.html'



class NickUpdateView(generic.UpdateView):
    model = models.Nick
    form_class = forms.NickForm
    pk_url_kwarg = "pk"


class CategoryListView(generic.ListView):
    model = models.Category
    form_class = forms.CategoryForm
    paginate_by = 20

class CategoryCreateView(generic.CreateView):
    model = models.Category
    form_class = forms.CategoryForm
    
class CategoryDetailView(generic.DetailView):
    model = models.Category
    form_class = forms.CategoryForm
    slug_url_kwarg = "slug"


class CategoryUpdateView(generic.UpdateView):
    model = models.Category
    form_class = forms.CategoryForm
    slug_url_kwarg = "slug"


class PostListView(generic.ListView):
    model = models.Post
    form_class = forms.PostForm
    paginate_by = 20


class PostCreateView(generic.CreateView):
    model = models.Post
    form_class = forms.PostForm


class PostDetailView(generic.DetailView):
    model = models.Post
    form_class = forms.PostForm


class PostUpdateView(generic.UpdateView):
    model = models.Post
    form_class = forms.PostForm
    pk_url_kwarg = "pk"
