# Generated by Django 3.2.6 on 2021-08-20 06:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0011_auto_20210819_1551'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='progress',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.userprogress'),
        ),
    ]
