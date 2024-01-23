# Generated by Django 5.0 on 2024-01-04 17:05

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0020_delete_message'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='image',
            field=models.FileField(upload_to=''),
        ),
        migrations.AlterField(
            model_name='recruiter',
            name='image',
            field=models.FileField(upload_to=''),
        ),
        migrations.AlterField(
            model_name='studentuser',
            name='image',
            field=models.FileField(upload_to=''),
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='job.job')),
                ('recipient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages_received', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
