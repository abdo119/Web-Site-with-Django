# Generated by Django 3.2.4 on 2021-07-08 16:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0007_alter_users_books'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='books',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='library.books'),
        ),
    ]
