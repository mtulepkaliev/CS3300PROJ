# Generated by Django 4.2.6 on 2023-11-17 18:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('task_tracker', '0011_alter_department_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='student',
            options={'permissions': (('manage_student', 'Manage student'),)},
        ),
    ]
