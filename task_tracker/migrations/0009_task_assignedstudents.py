# Generated by Django 4.2.6 on 2023-11-17 15:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task_tracker', '0008_department_leadergroup_department_membergroup'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='assignedStudents',
            field=models.ManyToManyField(blank=True, related_name='assignedTasks', to='task_tracker.student'),
        ),
    ]
