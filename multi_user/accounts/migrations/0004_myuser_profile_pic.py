# Generated by Django 4.1.1 on 2022-10-03 14:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_appointment'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuser',
            name='profile_pic',
            field=models.FileField(blank=True, null=True, upload_to='images'),
        ),
    ]
