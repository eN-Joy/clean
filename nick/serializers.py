from rest_framework import serializers

from . import models


class NickSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Nick
        fields = [
            "name",
            "gender",
        ]

class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Category
        fields = [
            "slug",
            "name",
        ]

class PostSerializer(serializers.ModelSerializer):

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
        ]
