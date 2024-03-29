# Generated by Django 4.2.3 on 2023-07-30 09:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sampleApp', '0003_category_cover_image'),
    ]

    operations = [
        migrations.RenameField(
            model_name='book',
            old_name='isbn_issn',
            new_name='isbn',
        ),
        migrations.RemoveField(
            model_name='book',
            name='call_number',
        ),
        migrations.RemoveField(
            model_name='book',
            name='edition',
        ),
        migrations.RemoveField(
            model_name='book',
            name='series_title',
        ),
        migrations.AddField(
            model_name='book',
            name='language',
            field=models.CharField(default='English', max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='book',
            name='year',
            field=models.IntegerField(blank=True, default=2022),
            preserve_default=False,
        ),
    ]
