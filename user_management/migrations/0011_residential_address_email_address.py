# Generated by Django 2.2.10 on 2022-06-17 10:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_management', '0010_auto_20220617_1045'),
    ]

    operations = [
        migrations.AddField(
            model_name='residential_address',
            name='email_address',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
