# Generated by Django 5.0.6 on 2024-09-15 23:19

import django.contrib.auth.models
import django.contrib.auth.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Adresse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ville', models.CharField(max_length=255)),
                ('commune', models.CharField(max_length=255)),
                ('quartier', models.CharField(max_length=255)),
                ('cellule', models.CharField(max_length=255)),
                ('avenue', models.CharField(max_length=255)),
                ('num_av', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Utilisateur',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('photo_url', models.URLField(blank=True, max_length=500, null=True)),
                ('user_type', models.CharField(choices=[('bailleur', 'Bailleur'), ('locataire', 'Locataire')], max_length=10)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='BienImmobilier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('surface', models.DecimalField(decimal_places=2, max_digits=10)),
                ('photo_url', models.URLField(blank=True, max_length=500, null=True)),
                ('description', models.TextField()),
                ('prix', models.DecimalField(decimal_places=2, max_digits=10)),
                ('adresse', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='pango_app.adresse')),
                ('utilisateur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='biens', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ContratLocation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_contrat', models.DateField()),
                ('date_debut', models.DateField()),
                ('prix', models.DecimalField(decimal_places=2, max_digits=10)),
                ('fichier', models.URLField(blank=True, max_length=500, null=True)),
                ('encours', models.BooleanField(default=False)),
                ('bien', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contrats', to='pango_app.bienimmobilier')),
                ('utilisateur', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='contrats', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Evenement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_evenement', models.CharField(choices=[('visite', 'Visite'), ('convocation', 'Convocation'), ('grace', 'Mesure de Grâce')], max_length=50)),
                ('date_debut', models.DateTimeField()),
                ('date_fin', models.DateTimeField()),
                ('description', models.TextField()),
                ('notifications', models.BooleanField(default=True)),
                ('modifier_jour', models.IntegerField(choices=[(15, '15 jours avant'), (10, '10 jours avant'), (5, '5 jours avant'), (1, '1 jour avant')], default=15)),
                ('vu_par_bailleur', models.BooleanField(default=False)),
                ('vu_par_locataire', models.BooleanField(default=False)),
                ('contrat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='evenements', to='pango_app.contratlocation')),
            ],
        ),
        migrations.CreateModel(
            name='FilMessagerie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contrat', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='fil_messagerie', to='pango_app.contratlocation')),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_heure', models.DateTimeField(auto_now_add=True)),
                ('contenu', models.TextField()),
                ('destinataire', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages_recus', to=settings.AUTH_USER_MODEL)),
                ('expediteur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages_envoyes', to=settings.AUTH_USER_MODEL)),
                ('fil_messagerie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='pango_app.filmessagerie')),
            ],
        ),
        migrations.CreateModel(
            name='Mot_cle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mot_cle', models.CharField(max_length=255)),
                ('contrat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mots_cles', to='pango_app.contratlocation')),
                ('locataire', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mots_cles', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Payement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('montant', models.DecimalField(decimal_places=2, max_digits=10)),
                ('date_payement', models.DateField()),
                ('moyen_payement', models.CharField(max_length=255)),
                ('contrat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payements', to='pango_app.contratlocation')),
            ],
        ),
    ]
