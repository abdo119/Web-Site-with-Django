# Generated by Django 3.2.4 on 2021-07-12 05:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0014_books_img'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='client',
            name='books',
        ),
        migrations.AddField(
            model_name='client',
            name='books',
            field=models.ManyToManyField(blank=True, null=True, to='library.Books'),
        ),
    ]