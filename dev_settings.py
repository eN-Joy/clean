SECRET_KEY = '^l)7d*%h&db4uft@dk%h-w&nup#pu%)a!d)c7jwgoixo5_hm0$'

DATABASES = {
    'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'dupfilter',
            'USER': 'zhou3594',
            'PASSWORD': 'mary7718',
            'HOST': 'sql',
            'PORT': '5432',
        },

    # 'default': {
    #         'ENGINE': 'django.db.backends.postgresql_psycopg2',
    #         'NAME': 'clean',
    #         'USER': 'zhou3594',
    #         'PASSWORD': 'mary7718',
    #         'HOST': 'sql',
    #         'PORT': '5432',
    #     }

    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    # }
}

# scrapy
REDIS_HOST = '127.0.0.1'
REDIS_URL = "redis://:e5UyadfZ$UhuDN!d8gL$eLo$YKB3thKm@127.0.0.1:6379"
REDIS_PASSWORD = 'e5UyadfZ$UhuDN!d8gL$eLo$YKB3thKm'