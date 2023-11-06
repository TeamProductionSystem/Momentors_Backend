# Generated by Django 4.1.7 on 2023-05-01 14:42

import multiselectfield.db.fields
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('team_production_system', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mentee',
            name='team_number',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='mentor',
            name='about_me',
            field=models.TextField(default='', max_length=1000),
        ),
        migrations.AlterField(
            model_name='mentor',
            name='skills',
            field=multiselectfield.db.fields.MultiSelectField(
                choices=[
                    ('HTML', 'HTML'),
                    ('CSS', 'CSS'),
                    ('JavaScript', 'JavaScript'),
                    ('React', 'React'),
                    ('Python', 'Python'),
                    ('Django', 'Django'),
                    ('Django REST', 'Django REST'),
                ],
                default='HTML',
                max_length=52,
            ),
        ),
    ]
