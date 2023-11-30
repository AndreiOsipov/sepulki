# Generated by Django 4.2.6 on 2023-11-27 07:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('kanban_app', '0002_alter_sepulka_square_or_small_alter_sepulka_state'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sepulka',
            name='fufelnitsa',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sepulka', to='kanban_app.fufelnitsa'),
        ),
        migrations.AlterField(
            model_name='sepulka',
            name='grymzik',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sepulka', to='kanban_app.grymzik'),
        ),
        migrations.AlterField(
            model_name='sepulka',
            name='shmurdik',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sepulka', to='kanban_app.shmurdik'),
        ),
    ]
