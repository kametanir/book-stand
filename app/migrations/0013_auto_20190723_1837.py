# Generated by Django 2.1.2 on 2019-07-23 09:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_auto_20190723_1829'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='renter',
            field=models.IntegerField(blank=True, choices=[(1, 'admin'), (2, '亀谷理恵')], null=True, verbose_name='貸出者'),
        ),
    ]
