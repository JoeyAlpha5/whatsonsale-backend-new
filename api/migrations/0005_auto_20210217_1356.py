# Generated by Django 3.1.6 on 2021-02-17 13:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20210211_1456'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postproduct',
            name='previous_price',
            field=models.FloatField(blank=True),
        ),
    ]
