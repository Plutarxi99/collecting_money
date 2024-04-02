# Generated by Django 5.0.3 on 2024-04-01 19:37

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Collect',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=120, verbose_name='Название сбора')),
                ('reason', models.PositiveSmallIntegerField(verbose_name='Причина сбора')),
                ('description', models.CharField(blank=True, max_length=1000, null=True, verbose_name='Описание сбора')),
                ('amount', models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(100000000, message='Сумма не может превышать 100 млн руб')], verbose_name='Сумма сбора')),
                ('amount_now', models.PositiveIntegerField(default=0, verbose_name='Сумма на данный момент')),
                ('count_people', models.PositiveIntegerField(default=0, verbose_name='Количество людей сделавших пожертвований')),
                ('photo', models.ImageField(blank=True, null=True, upload_to='collect/', verbose_name='обложка сбора')),
                ('end_of_event', models.DateTimeField(verbose_name='Конец сбора')),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='author', to=settings.AUTH_USER_MODEL)),
                ('donates', models.ManyToManyField(blank=True, null=True, related_name='donates', to=settings.AUTH_USER_MODEL, verbose_name='Донатеры')),
            ],
            options={
                'verbose_name': 'Групповой сбор',
                'verbose_name_plural': 'Групповые сборы',
            },
        ),
    ]