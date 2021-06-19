# Generated by Django 3.1.7 on 2021-06-19 17:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('GamerMatch', '0009_personalgames'),
    ]

    operations = [
        migrations.AlterField(
            model_name='personaltags',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
