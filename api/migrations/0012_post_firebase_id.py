# Generated by Django 3.1.6 on 2021-04-10 13:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_useraccount_push_token'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='firebase_id',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
