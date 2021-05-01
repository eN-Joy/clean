# redis_to_django.py

# -*- coding: utf-8 -*-
# initialize django
import os
import sys
import django
import json
import redis
import pytz
from datetime import datetime

sys.path.append('/home/zhou3594/workspace/clean')
os.environ['DJANGO_SETTINGS_MODULE'] = 'clean.settings'
django.setup()

from nick.models import Nick, Category, Post
from django.db import IntegrityError

try:
    from dev_settings import *
except ImportError:
    pass


def save_page(item):
    def get_nick(**kwargs):
        nick, created = Nick.objects.get_or_create(
            name=kwargs['nick'],
            defaults={
                'gender': None if kwargs['gender'] is None else bool(kwargs['gender'])
            })
        return nick  # return a nick object

    nicks = dict([(nick['nick'], get_nick(**nick)) for nick in item['nicks']])

    if not '»' in item['cat_name']:
        category, created = Category.objects.update_or_create(
            name=item['cat_name'],
            defaults={
                'slug': item['cat_slug'],
                'parent': None,
            })

    else:
        parent_category, created = Category.objects.get_or_create(
            name=item['cat_name'].split('»')[0],
        )
        category, created = Category.objects.get_or_create(
            name=item['cat_name'].split('»')[1],
            defaults={
                'slug': item['cat_slug'],
                'parent': parent_category,
            })

    # start to build list of posts, to start with op
    post_list = [post for post in item['threads']
                 if post['reply_to'] == None]
    post_obj_list = {}

    while post_list:
        posts = [
            Post(
                title=p['title'],
                category=category,
                url=p['url'],
                nick=nicks[p['nick']],  # what index?
                post_date=pytz.utc.localize(
                    datetime.strptime(p['post_date'], "%m/%d/%Y %H:%M:%S")),
                bytes=p['bytes'],
                hits=0,
                votes=0,
                reply_to=None if (
                    not post_obj_list) else post_obj_list[p['reply_to']]
            )
            for p in post_list
        ]

        # decouple this into main method
        # post_obj_list = dict(zip(
        #     [post['url'] for post in post_list],
        #     # Post.objects.bulk_create(posts, ignore_conflicts=True)
        #     Post.objects.bulk_create(posts)
        # ))

        try:
            post_obj_list = dict(zip(
                [post['url'] for post in post_list],
                # Post.objects.bulk_create(posts, ignore_conflicts=True)
                Post.objects.bulk_create(posts)
            ))
        except IntegrityError:
            for p in post_list:
                post_obj_list[p['url']] = Post.objects.get_or_create(
                    title=p['title'],
                    category=category,
                    url=p['url'],
                    nick=nicks[p['nick']],  # what index?
                    post_date=pytz.utc.localize(
                        datetime.strptime(p['post_date'], "%m/%d/%Y %H:%M:%S")),
                    bytes=p['bytes'],
                    hits=0,
                    votes=0,
                    reply_to=None if (
                        not post_obj_list) else post_obj_list[p['reply_to']]
                )[0]

            # post_obj_list = dict(zip(
            #     [post['url'] for post in post_list],
            #     [Post.objects.get_or_create(*post) for post in posts]
            # ))

        remained_post_list = [
            post for post in item['threads'] if post not in post_list]
        post_list = [
            post for post in remained_post_list if post['reply_to'] in post_obj_list.keys()]


def main():
    # 指定redis数据库信息
    rediscli = redis.StrictRedis(
        host=REDIS_HOST, port=6379, db=0, password=REDIS_PASSWORD)

    # host='127.0.0.1', port=6379, db=0, password='e5UyadfZ$UhuDN!d8gL$eLo$YKB3thKm')

    while True:
        # FIFO模式为 blpop，LIFO模式为 brpop，获取键值
        source, data = rediscli.blpop(["mpage:items"])
        item = json.loads(data)
        try:
            save_page(item)
            print(
                '###############################################################################')
            print('Page %s has been processed by %s' %
                  (item['page_url'], item['crawler']))
            print(
                '###############################################################################')
        except (IntegrityError, ValueError) as e:
            print(
                '###############################################################################')
            print('Page %s has value error %s' %
                  (item['page_url'], e))
            print(
                '###############################################################################')


if __name__ == '__main__':
    main()
