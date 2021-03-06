# Generated by Django 3.1 on 2020-08-20 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='book_locate',
            field=models.BooleanField(choices=[(0, '新校区'), (1, '老校区')], default=0, max_length=1),
        ),
        migrations.AddField(
            model_name='book',
            name='sale_way',
            field=models.BooleanField(choices=[(0, '出租'), (1, '出售')], default=0, max_length=1),
        ),
        migrations.AlterField(
            model_name='book',
            name='contact_number',
            field=models.CharField(max_length=40, verbose_name='联系方式'),
        ),
    ]
