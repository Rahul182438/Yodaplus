# Generated by Django 3.2.6 on 2021-08-25 07:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0002_alter_verificationstatus_email_otp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='verificationstatus',
            name='email_otp',
            field=models.CharField(max_length=50),
        ),
    ]
