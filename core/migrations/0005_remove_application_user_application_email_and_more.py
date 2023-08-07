# Generated by Django 4.2.4 on 2023-08-06 20:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_application'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='application',
            name='user',
        ),
        migrations.AddField(
            model_name='application',
            name='email',
            field=models.EmailField(default='prosper@gmail.com', max_length=254),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='application',
            name='username',
            field=models.CharField(default='prosper', max_length=100),
            preserve_default=False,
        ),
    ]
