# Generated by Django 5.0.6 on 2024-10-20 23:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pango_app', '0008_alter_mot_cle_locataire'),
    ]

    operations = [
        migrations.AddField(
            model_name='mot_cle',
            name='email',
            field=models.EmailField(max_length=254, null=True),
        ),
    ]
