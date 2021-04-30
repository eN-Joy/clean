from rest_framework import viewsets, permissions

from . import serializers
from . import models


class NickViewSet(viewsets.ModelViewSet):
    """ViewSet for the Nick class"""

    queryset = models.Nick.objects.all()
    serializer_class = serializers.NickSerializer
    permission_classes = [permissions.IsAuthenticated]


class CategoryViewSet(viewsets.ModelViewSet):
    """ViewSet for the Category class"""

    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer
    permission_classes = [permissions.IsAuthenticated]


class PostViewSet(viewsets.ModelViewSet):
    """ViewSet for the Post class"""

    queryset = models.Post.objects.all()
    serializer_class = serializers.PostSerializer
    permission_classes = [permissions.IsAuthenticated]
