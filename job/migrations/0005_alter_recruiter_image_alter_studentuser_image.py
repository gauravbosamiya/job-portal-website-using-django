# Generated by Django 5.0 on 2023-12-26 03:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0004_alter_studentuser_image_recruiter'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recruiter',
            name='image',
            field=models.ImageField(upload_to='profile/bg_images/'),
        ),
        migrations.AlterField(
            model_name='studentuser',
            name='image',
            field=models.ImageField(upload_to='profile/bg_images/'),
        ),
    ]