# Generated by Django 3.1 on 2020-08-21 01:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0002_auto_20200820_2206'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='book_locate',
            field=models.BooleanField(choices=[(0, '新校区'), (1, '老校区')], default=0, max_length=1, verbose_name='藏书位置'),
        ),
        migrations.AlterField(
            model_name='book',
            name='sale_way',
            field=models.BooleanField(choices=[(0, '出售'), (1, '出租')], max_length=1, verbose_name='方式'),
        ),
    ]