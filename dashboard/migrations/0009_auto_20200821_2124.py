# Generated by Django 3.1 on 2020-08-21 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0008_auto_20200821_2014'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='videos',
            field=models.TextField(default='#', null=True, verbose_name='视频链接'),
        ),
    ]
