# Generated by Django 5.0 on 2023-12-26 18:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0007_job'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='creation_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]