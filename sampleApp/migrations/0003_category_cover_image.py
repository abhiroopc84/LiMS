# Generated by Django 4.2.3 on 2023-07-30 08:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sampleApp', '0002_rename_books_book_remove_user_cart_books'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='cover_image',
            field=models.ImageField(default=1, upload_to='categories/'),
            preserve_default=False,
        ),
    ]
