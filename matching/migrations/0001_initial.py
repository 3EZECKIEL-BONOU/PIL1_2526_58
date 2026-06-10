# Generated migration for matching app - clean version

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CreneauHoraire',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('jour', models.CharField(choices=[('Lundi', 'Lundi'), ('Mardi', 'Mardi'), ('Mercredi', 'Mercredi'), ('Jeudi', 'Jeudi'), ('Vendredi', 'Vendredi'), ('Samedi', 'Samedi'), ('Dimanche', 'Dimanche')], max_length=20)),
                ('periode', models.CharField(max_length=50)),
            ],
            options={'db_table': 'crenaux_horaires'},
        ),
        migrations.CreateModel(
            name='Matiere',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom_matiere', models.CharField(max_length=150, unique=True)),
            ],
            options={'db_table': 'matieres'},
        ),
        migrations.CreateModel(
            name='Utilisateur',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=100)),
                ('prenom', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=100, unique=True)),
                ('telephone', models.CharField(max_length=150, unique=True)),
                ('mot_de_passe', models.CharField(max_length=255)),
                ('filiere', models.CharField(choices=[('Génie Logiciel', 'Génie Logiciel'), ('Intelligence Artificielle', 'Intelligence Artificielle'), ('Internet et multimédia', 'Internet et multimédia'), ('Sécurité Informatique', 'Sécurité Informatique')], max_length=50)),
                ('niveau_etudes', models.CharField(choices=[('License 1', 'License 1'), ('License 2', 'License 2'), ('License 3', 'License 3'), ('Master 1', 'Master 1'), ('Master 2', 'Master 2'), ('Master 3', 'Master 3')], max_length=50)),
                ('photo_profil', models.CharField(blank=True, max_length=255, null=True)),
                ('bio', models.TextField(blank=True, null=True)),
                ('date_inscription', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={'db_table': 'utilisateurs'},
        ),
        migrations.CreateModel(
            name='AnnonceMentorat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_annonce', models.CharField(choices=[('offre', 'Offre'), ('demande', 'Demande')], max_length=20)),
                ('format_propose', models.CharField(choices=[('présentiel', 'Présentiel'), ('en ligne', 'En ligne')], max_length=20)),
                ('description', models.TextField(blank=True, null=True)),
                ('date_publication', models.DateTimeField(auto_now_add=True)),
                ('matiere', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='matching.matiere')),
                ('auteur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='annonces', to='matching.utilisateur')),
            ],
            options={'db_table': 'annonces_mentorat'},
        ),
        migrations.CreateModel(
            name='ReponsesOffre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField(blank=True, null=True)),
                ('date_response', models.DateTimeField(auto_now_add=True)),
                ('annonce', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reponses', to='matching.annoncementorat')),
                ('postulant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reponses_envoyees', to='matching.utilisateur')),
            ],
            options={'db_table': 'reponses_offre'},
        ),
        migrations.CreateModel(
            name='ProgrammeEtudes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filiere', models.CharField(choices=[('Génie Logiciel', 'Génie Logiciel'), ('Intelligence Artificielle', 'Intelligence Artificielle'), ('Internet et multimédia', 'Internet et multimédia'), ('Sécurité Informatique', 'Sécurité Informatique')], max_length=50)),
                ('niveau_etudes', models.CharField(choices=[('License 1', 'License 1'), ('License 2', 'License 2'), ('License 3', 'License 3'), ('Master 1', 'Master 1'), ('Master 2', 'Master 2'), ('Master 3', 'Master 3')], max_length=50)),
                ('matiere', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='matching.matiere')),
            ],
            options={'db_table': 'programme_etudes', 'unique_together': {('filiere', 'niveau_etudes', 'matiere')}},
        ),
        migrations.CreateModel(
            name='UtilisateurCompetence',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('matiere', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='matching.matiere')),
                ('utilisateur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='competences', to='matching.utilisateur')),
            ],
            options={'db_table': 'utilisateur_competences', 'unique_together': {('utilisateur', 'matiere')}},
        ),
        migrations.CreateModel(
            name='UtilisateurDisponibilite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creneau', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='matching.creneauhoraire')),
                ('utilisateur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='disponibilites', to='matching.utilisateur')),
            ],
            options={'db_table': 'utilisateur_disponibilites', 'unique_together': {('utilisateur', 'creneau')}},
        ),
        migrations.CreateModel(
            name='UtilisateurLacune',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('matiere', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='matching.matiere')),
                ('utilisateur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lacunes', to='matching.utilisateur')),
            ],
            options={'db_table': 'utilisateur_lacunes', 'unique_together': {('utilisateur', 'matiere')}},
        ),
        migrations.CreateModel(
            name='Profil',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio', models.TextField(blank=True)),
                ('filiere', models.CharField(max_length=100, blank=True)),
                ('niveau', models.CharField(max_length=50, blank=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profil', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Matching',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.FloatField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('etudiant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='match_etudiant', to=settings.AUTH_USER_MODEL)),
                ('mentor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='match_mentor', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
