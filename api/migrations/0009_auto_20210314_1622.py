# Generated by Django 3.1.6 on 2021-03-14 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_postcomment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useraccount',
            name='profile_image',
            field=models.FileField(upload_to='profilePic'),
        ),
    ]
