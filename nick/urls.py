from django.urls import path, include
from rest_framework import routers

from . import api
from . import views


router = routers.DefaultRouter()
router.register("Nick", api.NickViewSet)
router.register("Category", api.CategoryViewSet)
router.register("Post", api.PostViewSet)

urlpatterns = (
    path("api/v1/", include(router.urls)),
    path("nick/Nick/", views.NickListView.as_view(), name="nick_Nick_list"),
    path("nick/Nick/create/", views.NickCreateView.as_view(), name="nick_Nick_create"),
    path("nick/Nick/detail/<int:pk>/", views.NickDetailView.as_view(), name="nick_Nick_detail"),
    path("nick/Nick/update/<int:pk>/", views.NickUpdateView.as_view(), name="nick_Nick_update"),
    path("nick/Category/", views.CategoryListView.as_view(), name="nick_Category_list"),
    path("nick/Category/create/", views.CategoryCreateView.as_view(), name="nick_Category_create"),
    path("nick/Category/detail/<slug:slug>/", views.CategoryDetailView.as_view(), name="nick_Category_detail"),
    path("nick/Category/update/<slug:slug>/", views.CategoryUpdateView.as_view(), name="nick_Category_update"),
    path("nick/Post/", views.PostListView.as_view(), name="nick_Post_list"),
    path("nick/Post/create/", views.PostCreateView.as_view(), name="nick_Post_create"),
    path("nick/Post/detail/<int:pk>/", views.PostDetailView.as_view(), name="nick_Post_detail"),
    path("nick/Post/update/<int:pk>/", views.PostUpdateView.as_view(), name="nick_Post_update"),
)
