# Generated by Django 2.2.9 on 2020-03-01 16:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0005_auto_20200228_2021'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='terms_confirmation',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
    ]
