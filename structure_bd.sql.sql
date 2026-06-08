CREATE TYPE liste_filieres AS ENUM ('Génie Logiciel', 'Intelligence Artificielle', 'Internet et multimédia', 'Sécurité informatique', 'Système embarqué et Internet des objets' );
CREATE TYPE liste_niveaux_etude AS ENUM ('Licence 1', 'Licence 2', 'Licence 3', 'Master 1', 'Master 2', 'Master 3');
CREATE TYPE format_cours AS ENUM ('présentiel', 'en ligne');
CREATE TYPE choix_annonce AS ENUM ('offre', 'demande');
CREATE TYPE statut_reponse AS ENUM ('en attente', 'accepté', 'refusé'); 
CREATE TYPE type_notification AS ENUM ('message', 'matching', 'système');
CREATE TYPE liste_jours_semaine AS ENUM ('Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche');

CREATE TABLE IF NOT EXISTS utilisateurs (id SERIAL PRIMARY KEY,
nom VARCHAR(100) NOT NULL,
prenom VARCHAR(100) NOT NULL,
email VARCHAR(100) UNIQUE NOT NULL,
telephone VARCHAR(150) UNIQUE NOT NULL,
mot_de_passe VARCHAR(255) NOT NULL,
filiere liste_filieres NOT NULL,
niveau_etudes liste_niveaux_etudes NOT NULL,
photo_profil VARCHAR(255) NULL,
bio TEXT NULL,
date_inscription TIMESTAMP DEFAULT CURRENT_TIMESTAMP);

CREATE TABLE IF NOT EXISTS matieres (id SERIAL PRIMARY KEY,
nom_matiere VARCHAR(150) UNIQUE NOT NULL);

CREATE TABLE IF NOT EXISTS crenaux_horaires (id SERIAL PRIMARY KEY,
jour liste_jours_semaine NOT NULL,
periode VARCHAR(50) NOT NULL);

CREATE TABLE IF NOT EXISTS programme_etudes (id SERIAL PRIMARY KEY,
filiere liste_filieres NOT NULL,
niveau_etudes liste_niveaux_etudes NOT NULL,
matiere_id INT REFERENCES matieres(id) ON DELETE CASCADE,
UNIQUE (filiere, niveau_etudes, matiere_id)
);

CREATE TABLE IF NOT EXISTS utilisateur_competences (utilisateur_id INT REFERENCES utilisateurs(id) ON DELETE CASCADE,
matiere_id INT REFERENCES matieres(id) ON DELETE CASCADE,
PRIMARY KEY (utilisateur_id, matiere_id));

CREATE TABLE IF NOT EXISTS utilisateur_lacunes (utilisateur_id INT REFERENCES utilisateurs(id) ON DELETE CASCADE,
matiere_id INT REFERENCES matieres(id) ON DELETE CASCADE,
PRIMARY KEY (utilisateur_id, matiere_id));

CREATE TABLE IF NOT EXISTS utilisateur_disponibilites (utilisateur_id INT REFERENCES utilisateurs(id) ON DELETE CASCADE,
creneau_id INT REFERENCES creneaux_horaires(id) ON DELETE CASCADE,
PRIMARY KEY (utilisateur_id, creneau_id));

CREATE TABLE IF NOT EXISTS annonces_mentorat (id SERIAL PRIMARY KEY,
auteur_id INT REFERENCES utilisateurs(id) ON DELETE CASCADE,
type_annonce choix_annonce NOT NULL,
matiere_id INT REFERENCES matieres(id) ON DELETE CASCADE,
format_propose format_cours NOT NULL,
description TEXT NULL,
date_publication TIMESTAMP DEFAULT CURRENT_TIMESTAMP);

CREATE TABLE IF NOT EXISTS reponses_offre (id SERIAL PRIMARY KEY,
annonce_id INT REFERENCES annonces_mentorat(id) ON DELETE CASCADE,
postulant_id INT REFERENCES utilisateurs(id) ON DELETE CASCADE,
statut statut_response DEFAULT 'en_attente',
message_accompagnement TEXT NULL,
date_response TIMESTAMP DEFAULT CURRENT_TIMESTAMP);

CREATE TABLE IF NOT EXISTS conversations (id SERIAL PRIMARY KEY,
createur_id INT REFERENCES utilisateurs(id) ON DELETE CASCADE,
destinataire_id INT REFERENCES utilisateurs(id) ON DELETE CASCADE,
date_envoi TIMESTAMP DEFAULT CURRENT_TIMESTAMP);

CREATE TABLE IF NOT EXISTS messages (id SERIAL PRIMARY KEY, 
conversation_id INT REFERENCES conversations(id) ON DELETE CASCADE,
expediteur_id INT REFERENCES utilisateurs(id) ON DELETE CASCADE
contenu TEXT NOT NULL,
date_envoi TIMESTAMP DEFAULT CURRENT_TIMESTAMP);

CREATE TABLE IF NOT EXISTS notifications (id SERIAL PRIMARY KEY,
utilisateur_id INT REFERENCES utilisaeurs(id) ON DELETE CASCADE,
type_notif type_notification NOT NULL,
contenu TEXT NOT NULL,
lu BOOLEAN DEFAULT FALSE,
date_notification TIMESTAMP DEFAULT CURRENT_TIMESTAMP);
