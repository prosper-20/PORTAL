# Generated by Django 4.2.4 on 2023-08-11 14:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_job_posted_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='company_name',
            field=models.CharField(default='Google', max_length=100),
            preserve_default=False,
        ),
    ]