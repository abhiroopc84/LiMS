# Generated by Django 4.2.3 on 2023-07-30 07:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sampleApp', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Books',
            new_name='Book',
        ),
        migrations.RemoveField(
            model_name='user',
            name='cart_books',
        ),
    ]