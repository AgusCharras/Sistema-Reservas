# Generated by Django 4.2.3 on 2023-07-04 23:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reservas', '0004_remove_servicio_incluido_servicio_nombre'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cabania',
            name='servicios',
        ),
        migrations.AddField(
            model_name='reserva',
            name='cabania',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='reservas.cabania'),
        ),
        migrations.AddField(
            model_name='reserva',
            name='servicios',
            field=models.ManyToManyField(to='reservas.servicio'),
        ),
        migrations.AlterField(
            model_name='complejo',
            name='cabania',
            field=models.ForeignKey(default='editar', on_delete=django.db.models.deletion.CASCADE, to='reservas.cabania'),
        ),
    ]
