# Generated by Django 2.1.2 on 2019-07-17 10:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0006_auto_20190717_1935'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='provider_by',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='提供者ID'),
        ),
        migrations.AlterField(
            model_name='item',
            name='provider',
            field=models.CharField(blank=True, default='', max_length=50, null=True, verbose_name='提供者'),
        ),
    ]