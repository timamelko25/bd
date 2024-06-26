# Generated by Django 5.0.4 on 2024-05-01 13:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0002_specialitydiscipline'),
    ]

    operations = [
        migrations.AlterField(
            model_name='specialitydiscipline',
            name='discipline',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='schedule.discipline'),
        ),
        migrations.AlterField(
            model_name='specialitydiscipline',
            name='speciality',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='schedule.speciality'),
        ),
        migrations.AlterField(
            model_name='student',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='schedule.group'),
        ),
        migrations.AlterField(
            model_name='student',
            name='speciality',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='schedule.speciality'),
        ),
    ]
