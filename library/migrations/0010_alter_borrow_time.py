# Generated by Django 3.2.4 on 2021-07-08 16:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0009_alter_books_publishedyear'),
    ]

    operations = [
        migrations.AlterField(
            model_name='borrow',
            name='time',
            field=models.IntegerField(),
        ),
    ]
