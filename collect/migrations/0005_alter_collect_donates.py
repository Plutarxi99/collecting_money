# Generated by Django 5.0.3 on 2024-04-02 08:16

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collect', '0004_alter_collect_donates'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='collect',
            name='donates',
            field=models.ManyToManyField(blank=True, null=True, related_name='donates', to=settings.AUTH_USER_MODEL, verbose_name='Донатеры'),
        ),
    ]