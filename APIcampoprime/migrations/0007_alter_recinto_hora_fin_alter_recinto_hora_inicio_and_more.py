# Generated by Django 4.2.13 on 2024-06-10 14:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('APIcampoprime', '0006_alter_recinto_hora_fin_alter_recinto_hora_inicio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recinto',
            name='hora_fin',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='recinto',
            name='hora_inicio',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='recinto',
            name='precio_por_hora',
            field=models.FloatField(),
        ),
    ]
