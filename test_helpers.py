import random
import string

from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import Group
from django.contrib.contenttypes.models import ContentType
from datetime import datetime

from nick import models as nick_models


def random_string(length=10):
    # Create a random string of length length
    letters = string.ascii_lowercase
    return "".join(random.choice(letters) for i in range(length))


def create_User(**kwargs):
    defaults = {
        "username": "%s_username" % random_string(5),
        "email": "%s_username@tempurl.com" % random_string(5),
    }
    defaults.update(**kwargs)
    return User.objects.create(**defaults)


def create_AbstractUser(**kwargs):
    defaults = {
        "username": "%s_username" % random_string(5),
        "email": "%s_username@tempurl.com" % random_string(5),
    }
    defaults.update(**kwargs)
    return AbstractUser.objects.create(**defaults)


def create_AbstractBaseUser(**kwargs):
    defaults = {
        "username": "%s_username" % random_string(5),
        "email": "%s_username@tempurl.com" % random_string(5),
    }
    defaults.update(**kwargs)
    return AbstractBaseUser.objects.create(**defaults)


def create_Group(**kwargs):
    defaults = {
        "name": "%s_group" % random_string(5),
    }
    defaults.update(**kwargs)
    return Group.objects.create(**defaults)


def create_ContentType(**kwargs):
    defaults = {
    }
    defaults.update(**kwargs)
    return ContentType.objects.create(**defaults)


def create_nick_Nick(**kwargs):
    defaults = {}
    defaults["name"] = ""
    defaults["gender"] = ""
    defaults.update(**kwargs)
    return nick_models.Nick.objects.create(**defaults)
def create_nick_Category(**kwargs):
    defaults = {}
    defaults["slug"] = ""
    defaults["name"] = ""
    defaults.update(**kwargs)
    return nick_models.Category.objects.create(**defaults)
def create_nick_Post(**kwargs):
    defaults = {}
    defaults["reply_to"] = ""
    defaults["bytes"] = ""
    defaults["url"] = ""
    defaults["votes"] = ""
    defaults["hits"] = ""
    defaults["post_date"] = datetime.now()
    defaults["title"] = ""
    if "nick" not in kwargs:
        defaults["nick"] = create_nick_Nick()
    if "category" not in kwargs:
        defaults["category"] = create_nick_Category()
    defaults.update(**kwargs)
    return nick_models.Post.objects.create(**defaults)
