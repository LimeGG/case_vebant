# Generated by Django 5.0.3 on 2024-03-09 22:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_userprofession_profession_active_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='markedcompetence',
            name='profession',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.profession'),
        ),
    ]
