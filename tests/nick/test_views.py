import pytest
import test_helpers

from django.urls import reverse
from django.test import Client


pytestmark = [pytest.mark.django_db]


def tests_Nick_list_view():
    instance1 = test_helpers.create_nick_Nick()
    instance2 = test_helpers.create_nick_Nick()
    client = Client()
    url = reverse("nick_Nick_list")
    response = client.get(url)
    assert response.status_code == 200
    assert str(instance1) in response.content.decode("utf-8")
    assert str(instance2) in response.content.decode("utf-8")


def tests_Nick_create_view():
    client = Client()
    url = reverse("nick_Nick_create")
    data = {
        "name": "text",
        "gender": true,
    }
    response = client.post(url, data)
    assert response.status_code == 302


def tests_Nick_detail_view():
    client = Client()
    instance = test_helpers.create_nick_Nick()
    url = reverse("nick_Nick_detail", args=[instance.pk, ])
    response = client.get(url)
    assert response.status_code == 200
    assert str(instance) in response.content.decode("utf-8")


def tests_Nick_update_view():
    client = Client()
    instance = test_helpers.create_nick_Nick()
    url = reverse("nick_Nick_update", args=[instance.pk, ])
    data = {
        "name": "text",
        "gender": true,
    }
    response = client.post(url, data)
    assert response.status_code == 302


def tests_Category_list_view():
    instance1 = test_helpers.create_nick_Category()
    instance2 = test_helpers.create_nick_Category()
    client = Client()
    url = reverse("nick_Category_list")
    response = client.get(url)
    assert response.status_code == 200
    assert str(instance1) in response.content.decode("utf-8")
    assert str(instance2) in response.content.decode("utf-8")


def tests_Category_create_view():
    client = Client()
    url = reverse("nick_Category_create")
    data = {
        "slug": "slug",
        "name": "text",
    }
    response = client.post(url, data)
    assert response.status_code == 302


def tests_Category_detail_view():
    client = Client()
    instance = test_helpers.create_nick_Category()
    url = reverse("nick_Category_detail", args=[instance.slug, ])
    response = client.get(url)
    assert response.status_code == 200
    assert str(instance) in response.content.decode("utf-8")


def tests_Category_update_view():
    client = Client()
    instance = test_helpers.create_nick_Category()
    url = reverse("nick_Category_update", args=[instance.slug, ])
    data = {
        "slug": "slug",
        "name": "text",
    }
    response = client.post(url, data)
    assert response.status_code == 302


def tests_Post_list_view():
    instance1 = test_helpers.create_nick_Post()
    instance2 = test_helpers.create_nick_Post()
    client = Client()
    url = reverse("nick_Post_list")
    response = client.get(url)
    assert response.status_code == 200
    assert str(instance1) in response.content.decode("utf-8")
    assert str(instance2) in response.content.decode("utf-8")


def tests_Post_create_view():
    nick = test_helpers.create_nick_Nick()
    category = test_helpers.create_nick_Category()
    client = Client()
    url = reverse("nick_Post_create")
    data = {
        "reply_to": 1,
        "bytes": 1,
        "url": 1,
        "votes": 1,
        "hits": 1,
        "post_date": datetime.now(),
        "title": "text",
        "nick": nick.pk,
        "category": category.pk,
    }
    response = client.post(url, data)
    assert response.status_code == 302


def tests_Post_detail_view():
    client = Client()
    instance = test_helpers.create_nick_Post()
    url = reverse("nick_Post_detail", args=[instance.pk, ])
    response = client.get(url)
    assert response.status_code == 200
    assert str(instance) in response.content.decode("utf-8")


def tests_Post_update_view():
    nick = test_helpers.create_nick_Nick()
    category = test_helpers.create_nick_Category()
    client = Client()
    instance = test_helpers.create_nick_Post()
    url = reverse("nick_Post_update", args=[instance.pk, ])
    data = {
        "reply_to": 1,
        "bytes": 1,
        "url": 1,
        "votes": 1,
        "hits": 1,
        "post_date": datetime.now(),
        "title": "text",
        "nick": nick.pk,
        "category": category.pk,
    }
    response = client.post(url, data)
    assert response.status_code == 302
