from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.functions import ExtractHour
from django.db.models import Count
from django.db.models.query import QuerySet
from django.urls import reverse
WXCBASE = 'https://bbs.wenxuecity.com'


class Nick(models.Model):

    # Fields
    name = models.CharField(max_length=20, db_index=True, unique=True)
    gender = models.BooleanField(null=True)


    class Meta:
        pass
    
    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse("nick_Nick_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("nick_Nick_update", args=(self.pk,))

    @property
    def number_of_post(self):
        return self.post_set.count()

    @property
    def posts_per_cat(self):
        return self.post_set.values('category__name')\
            .annotate(post_count=Count('category'))\
            .order_by('-post_count')

    @property
    def posts_per_hour(self):
        return self.post_set.annotate(
            hour=ExtractHour('post_date')).values('hour').annotate(hour_count=Count('hour')).order_by('hour')

    # @property
    # def reply_to(self):
    #     # pitfall: if user replied more than once, only one count accrue...
    #     return Post.objects.filter(url__in=self.post_set.values('reply_to__url'))\
    #         .values('nick__name')\
    #         .annotate(reply_to_count=Count('nick__name'))\
    #         .order_by('-reply_to_count')

    @property
    def reply_to(self):
        return self.post_set.values('reply_to__nick__name')\
            .values('reply_to__nick__name')\
            .annotate(reply_to_count=Count('reply_to__nick__name'))\
            .order_by('-reply_to_count')[:5]


    @property
    def replied_by(self):
        return Post.objects.filter(reply_to__in=self.post_set.all())\
            .values('nick__name')\
            .annotate(replied_by_count=Count('nick__name'))\
            .order_by('-replied_by_count')[:5]

class Category(models.Model):

    # Fields
    slug = models.SlugField(max_length=20)
    name = models.CharField(max_length=20, unique=True)
    parent = models.ForeignKey(
        'self', null=True, default=None, on_delete=CASCADE)

    class Meta:
        pass

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse("nick_Category_detail", args=(self.slug,))

    def get_update_url(self):
        return reverse("nick_Category_update", args=(self.slug,))


class Post(models.Model):

    # Relationships
    nick = models.ForeignKey("nick.Nick", on_delete=models.CASCADE)
    category = models.ForeignKey("nick.Category", on_delete=models.CASCADE)
    reply_to = models.ForeignKey(
        'self', null=True, default=None, on_delete=CASCADE)
    # reply_to = models.IntegerField(null=True)

    bytes = models.IntegerField()
    url = models.IntegerField(db_index=True)
    votes = models.IntegerField(null=True, blank=True)
    hits = models.IntegerField(null=True, blank=True)
    post_date = models.DateTimeField(null=True, blank=True)
    title = models.CharField(max_length=120)

    class Meta:
        ordering = ['-post_date']
        unique_together = ['category', 'url']

    def __str__(self):
        return str(self.title)

    def get_absolute_url(self):
        return reverse("nick_Post_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("nick_Post_update", args=(self.pk,))

    @property
    def source_url(self):
        # return reverse("nick_Post_detail", args=(self.pk,))
        return f'{WXCBASE}/{self.category.slug}/{self.url}.html'

    @property
    def is_op(self):
        return not bool(self.reply_to)
