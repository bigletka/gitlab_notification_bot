# Generated by Django 4.2.2 on 2023-06-19 12:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GitLab',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chat_id', models.TextField(unique=True)),
                ('json', models.JSONField()),
            ],
        ),
    ]
