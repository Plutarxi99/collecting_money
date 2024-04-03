# Generated by Django 5.0.3 on 2024-04-03 08:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collect', '0007_alter_collect_donates'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collect',
            name='reason',
            field=models.PositiveSmallIntegerField(choices=[(0, 'День рожденья'), (1, 'Свадьба'), (2, 'Стартап')], verbose_name='Причина сбора'),
        ),
    ]
