# Generated by Django 4.2.13 on 2024-05-23 21:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_alter_course_course_pdf'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quiz_desc',
            name='quiz_id',
            field=models.CharField(max_length=200, primary_key=True, serialize=False),
        ),
    ]
