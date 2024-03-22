# Generated by Django 4.2.4 on 2024-03-21 12:38

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('reservas', '0021_reservaservicio_precio_original_servicio'),
    ]

    operations = [
        migrations.AddField(
            model_name='servicio',
            name='codigoServicio',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
    ]
