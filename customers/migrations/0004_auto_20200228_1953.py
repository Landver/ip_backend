# Generated by Django 2.2.9 on 2020-02-28 19:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0003_auto_20200228_1952'),
    ]

    operations = [
        migrations.AlterField(
            model_name='enrolmentrequest',
            name='approved',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]
