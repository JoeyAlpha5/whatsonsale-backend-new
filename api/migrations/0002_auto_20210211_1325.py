# Generated by Django 2.2.1 on 2021-02-11 13:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='brand',
            name='logo',
            field=models.URLField(),
        ),
        migrations.AlterField(
            model_name='brand',
            name='website',
            field=models.URLField(),
        ),
        migrations.AlterField(
            model_name='post',
            name='post_cover',
            field=models.URLField(),
        ),
        migrations.AlterField(
            model_name='postcatalogue',
            name='image',
            field=models.URLField(),
        ),
        migrations.AlterField(
            model_name='postproduct',
            name='image',
            field=models.URLField(),
        ),
    ]