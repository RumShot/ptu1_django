# Generated by Django 4.0.4 on 2022-05-11 13:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0003_alter_book_isbn_bookinstance'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='author',
            options={'ordering': ['last_name', 'first_name'], 'verbose_name': 'autorius', 'verbose_name_plural': 'autoriai'},
        ),
        migrations.AlterModelOptions(
            name='bookinstance',
            options={'ordering': ['due_back'], 'verbose_name': 'knygos kopija', 'verbose_name_plural': 'knygu kopijos'},
        ),
    ]
