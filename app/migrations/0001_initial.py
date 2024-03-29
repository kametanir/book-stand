# Generated by Django 2.1.2 on 2019-07-09 10:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('book_name', models.CharField(default='', max_length=100, verbose_name='書籍名')),
                ('description', models.TextField(blank=True, null=True, verbose_name='書籍説明')),
                ('provider', models.CharField(default='', max_length=50, verbose_name='提供者')),
                ('provide_start_date', models.DateField(default=django.utils.timezone.now, verbose_name='提供開始日')),
                ('rent_status', models.IntegerField(choices=[(10, '貸出可能'), (20, '貸出中'), (30, '提供終了')], default=10, verbose_name='貸出ステータス')),
                ('created_at', models.DateTimeField(blank=True, editable=False, null=True, verbose_name='作成時間')),
                ('updated_at', models.DateTimeField(blank=True, editable=False, null=True, verbose_name='更新時間')),
                ('created_by', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='CreatedBy', to=settings.AUTH_USER_MODEL, verbose_name='作成者')),
                ('updated_by', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='UpdatedBy', to=settings.AUTH_USER_MODEL, verbose_name='更新者')),
            ],
            options={
                'verbose_name': 'ブックスタンドマネージャー',
                'verbose_name_plural': 'ブックスタンドマネージャー',
            },
        ),
    ]
