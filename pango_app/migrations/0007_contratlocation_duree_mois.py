# Generated by Django 5.0.6 on 2024-10-20 23:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pango_app', '0006_alter_bienimmobilier_surface'),
    ]

    operations = [
        migrations.AddField(
            model_name='contratlocation',
            name='duree_mois',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
