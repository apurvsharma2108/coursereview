# Generated by Django 3.0.8 on 2020-11-20 17:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_auto_20200922_2158'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='Rating',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='course',
            name='financial_aid',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='course',
            name='year',
            field=models.IntegerField(default=0),
        ),
    ]
