# Generated by Django 5.0.3 on 2024-03-30 19:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasktrackerapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='description',
            field=models.TextField(blank=True),
        ),
    ]
