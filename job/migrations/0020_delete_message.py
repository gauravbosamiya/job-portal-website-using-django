# Generated by Django 5.0 on 2024-01-04 13:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0019_message'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Message',
        ),
    ]