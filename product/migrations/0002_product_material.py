# Generated by Django 4.1.7 on 2023-04-03 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='material',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
