# Generated by Django 4.2.4 on 2023-08-11 16:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_profile_is_employer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='username',
            field=models.CharField(default='bella', max_length=100),
            preserve_default=False,
        ),
    ]
