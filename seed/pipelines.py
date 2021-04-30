# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import logging
import time
from datetime import datetime
import pytz

from django.db import IntegrityError
from nick.models import Nick, Category, Post


class SeedPipeline:
    def process_item(self, item, spider):
        return item


class SavePagePipeline(object):
    def process_item(self, item, spider):

        # what to take as input? a single dict with two keys `nick` and `gender`
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
                    reply_to=None if (not post_obj_list) else post_obj_list[p['reply_to']]
                )
                for p in post_list
            ]

            try:
                post_obj_list = dict(zip(
                    [post['url'] for post in post_list],
                    # Post.objects.bulk_create(posts, ignore_conflicts=True)
                    Post.objects.bulk_create(posts)
                ))
            except IntegrityError as e:
                pass

            remained_post_list = [post for post in item['threads'] if post not in post_list]
            post_list = [post for post in remained_post_list if post['reply_to'] in post_obj_list.keys()]
            
        return item


class SaveDjangoPipeline(object):
    def process_item(self, item, spider):
        def save_post(**kwargs):
            nick, created = Nick.objects.get_or_create(
                name=kwargs['nick'],
                defaults={
                    'gender': None if kwargs['gender'] is None else bool(kwargs['gender'])
                })

            if not '»' in kwargs['cat_name']:
                category, created = Category.objects.update_or_create(
                    name=kwargs['cat_name'],
                    defaults={
                        'slug': kwargs['cat_slug'],
                        'parent': None,
                    })

            else:
                parent_category, created = Category.objects.get_or_create(
                    name=kwargs['cat_name'].split('»')[0],
                )
                category, created = Category.objects.get_or_create(
                    name=kwargs['cat_name'].split('»')[1],
                    defaults={
                        'slug': kwargs['cat_slug'],
                        'parent': parent_category,
                    })

            try:
                post, created = Post.objects.get_or_create(
                    title=kwargs['title'],
                    category=category,
                    defaults={
                        'url': kwargs['url'],
                        'post_date': pytz.utc.localize(
                            datetime.strptime(kwargs['post_date'], "%m/%d/%Y %H:%M:%S")),
                        'nick': nick,
                        # is_op :  None if kwargs['is_op'] is None else bool(kwargs['is_op']),
                        'bytes': kwargs['bytes'],
                        'hits': kwargs['hits'],
                        'votes': kwargs['votes'],
                        # 'reply_to': reply_to,
                        'reply_to': None if kwargs['reply_to'] is None else save_post(**kwargs['reply_to']),
                    }
                )
                return post

            except IntegrityError:
                logging.info(
                    "The post %s has been processed previously" % kwargs['url'])
                return None
        save_post(**item)
        return item


class NickDjangoPipeline(object):
    def process_item(self, item, spider):
        # function approach again:
        def save_nick(**kwargs):
            nick, created = Nick.objects.get_or_create(
                name=kwargs['nick'],
                defaults={
                    'gender': None if kwargs['gender'] is None else bool(kwargs['gender'])
                })
            return nick

        def save_category(**kwargs):
            if not '»' in kwargs['cat_name']:
                category, created = Category.objects.update_or_create(
                    name=kwargs['cat_name'],
                    defaults={
                        'slug': kwargs['cat_slug'],
                        'parent': None,
                    })

            else:
                parent_category, created = Category.objects.get_or_create(
                    name=kwargs['cat_name'].split('»')[0],
                )
                category, created = Category.objects.get_or_create(
                    name=kwargs['cat_name'].split('»')[1],
                    defaults={
                        'slug': kwargs['cat_slug'],
                        'parent': parent_category,
                    })
            return category

        def save_reply(**kwargs):
            try:
                post, created = Post.objects.get_or_create(
                    title=kwargs['title'],
                    category=save_category(**kwargs),
                    defaults={
                        'url': kwargs['url'],
                        'post_date': pytz.utc.localize(
                            datetime.strptime(kwargs['post_date'], "%m/%d/%Y %H:%M:%S")),
                        'nick': save_nick(**kwargs),
                        # is_op :  None if kwargs['is_op'] is None else bool(kwargs['is_op']),
                        'bytes': kwargs['bytes'],
                        'hits': kwargs['hits'],
                        'votes': kwargs['votes'],
                        # 'reply_to': reply_to,
                        'reply_to': None,
                    }
                )
                return post
            except IntegrityError:
                logging.info(
                    "The post %s has been processed previously" % kwargs['url'])
                return None

        def save_post(**kwargs):
            try:
                post, created = Post.objects.get_or_create(
                    title=kwargs['title'],
                    category=save_category(**kwargs),
                    defaults={
                        'url': kwargs['url'],
                        'post_date': pytz.utc.localize(
                            datetime.strptime(kwargs['post_date'], "%m/%d/%Y %H:%M:%S")),
                        'nick': save_nick(**kwargs),
                        # is_op :  None if kwargs['is_op'] is None else bool(kwargs['is_op']),
                        'bytes': kwargs['bytes'],
                        'hits': kwargs['hits'],
                        'votes': kwargs['votes'],
                        # 'reply_to': reply_to,
                        'reply_to': None if kwargs['reply_to'] is None else save_reply(**kwargs['reply_to']),
                    }
                )
                return post
            except IntegrityError:
                logging.info(
                    "The post %s has been processed previously" % kwargs['url'])
                return None

        # if item['reply_to'] is None:
        #     save_post(**item)
        # else:
        #     reply = save_reply(**item)
        #     save_post(**item, reply=reply)
        save_post(**item)
        return item
