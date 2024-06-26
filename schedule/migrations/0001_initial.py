# Generated by Django 5.0.4 on 2024-04-29 12:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Discipline',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('exam', models.CharField(choices=[('зачет', 'зачет'), ('экзамен', 'экзамен')], max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Speciality',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group_number', models.CharField(max_length=255, unique=True)),
                ('speciality', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='schedule.speciality')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('study_year', models.CharField(max_length=255)),
                ('is_studying', models.BooleanField(default=True)),
                ('is_gradueted', models.BooleanField(default=False)),
                ('is_expelled', models.BooleanField(default=False)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='schedule.group')),
                ('speciality', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='schedule.speciality')),
            ],
        ),
        migrations.CreateModel(
            name='Teachers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('study_discipline', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='schedule.discipline')),
            ],
        ),
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('semestr', models.CharField(max_length=255)),
                ('year', models.CharField(max_length=255)),
                ('mark', models.CharField(choices=[('незачет', 'незачет'), ('зачет', 'зачет'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')], max_length=255)),
                ('discipline', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='schedule.discipline')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='schedule.student')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='schedule.teachers')),
            ],
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('semester', models.CharField(max_length=255)),
                ('discipline', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='schedule.discipline')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='schedule.group')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='schedule.teachers')),
            ],
        ),
    ]
