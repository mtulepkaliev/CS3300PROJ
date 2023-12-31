# Generated by Django 4.2.6 on 2023-10-26 19:51

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('summary', models.CharField(max_length=200)),
                ('detail', models.TextField(max_length=1000)),
                ('is_complete', models.BooleanField(default=False)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('deadline', models.DateTimeField(blank=True, null=True)),
                ('department', models.CharField(choices=[('All', 'ALL'), ('EE', 'Electrical'), ('MECH', 'Mechanical'), ('BUS', 'Business')], default='All', max_length=200)),
            ],
        ),
    ]
