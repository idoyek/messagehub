# Generated by Django 5.0.2 on 2024-02-15 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_message_delete_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='is_read',
            field=models.BooleanField(default=False),
        ),
    ]