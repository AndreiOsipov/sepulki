# Generated by Django 4.2.6 on 2023-11-29 23:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kanban_app', '0005_alter_sepulka_fufelnitsa_alter_sepulka_grymzik'),
    ]

    operations = [
        migrations.AddField(
            model_name='sepulka',
            name='datetime_proccessd',
            field=models.DateField(blank=True, null=True),
        ),
    ]
