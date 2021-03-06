# Generated by Django 3.2 on 2021-05-01 18:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField()),
                ('name', models.CharField(max_length=50, unique=True)),
                ('parent', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='nick.category')),
            ],
        ),
        migrations.CreateModel(
            name='Nick',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=50, unique=True)),
                ('gender', models.BooleanField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bytes', models.IntegerField()),
                ('url', models.IntegerField(db_index=True)),
                ('votes', models.IntegerField(blank=True, null=True)),
                ('hits', models.IntegerField(blank=True, null=True)),
                ('post_date', models.DateTimeField(blank=True, null=True)),
                ('title', models.CharField(max_length=120)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nick.category')),
                ('nick', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nick.nick')),
                ('reply_to', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='nick.post')),
            ],
            options={
                'ordering': ['-post_date'],
                'unique_together': {('category', 'url')},
            },
        ),
    ]
