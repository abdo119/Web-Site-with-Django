# Generated by Django 3.2.4 on 2021-07-12 03:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0013_rename_user_client'),
    ]

    operations = [
        migrations.AddField(
            model_name='books',
            name='img',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
