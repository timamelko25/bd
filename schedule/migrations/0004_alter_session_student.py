# Generated by Django 5.0.4 on 2024-05-01 13:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0003_alter_specialitydiscipline_discipline_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='session',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='schedule.student'),
        ),
    ]
