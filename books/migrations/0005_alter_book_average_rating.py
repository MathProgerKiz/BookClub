# Generated by Django 4.2.15 on 2024-08-24 21:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0004_alter_book_average_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='average_rating',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
