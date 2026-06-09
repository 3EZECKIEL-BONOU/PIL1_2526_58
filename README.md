# CAHIER DES CHARGES

## THÈME : « INTÉGRATION EFFICACE DU NUMÉRIQUE DANS L'APPRENTISSAGE »
## PROJET : IFRI_MentorLink

---

## SOMMAIRE
1. Nom de l'équipe
2. Présentations des membres
3. PROBLÈME IDENTIFIÉ
4. DESCRIPTION DE LA SOLUTION
5. Exigences fonctionnelles
   - Module public
   - Module authentification
   - Dashboard étudiant
   - Dashboard entreprise / Mentor
6. Technologies utilisées
   - Frontend
   - Frameworks et bibliothèques
   - Backend (phase 2)
   - Sécurité
7. MODÈLE ÉCONOMIQUE
8. Perspectives et évolutions futures
9. Architecture et faisabilité technique
   - Architecture générale
   - Composants principaux
   - Faisabilité technique

---

## 1. Nom de l'équipe
**GROUPE 58 IFRI2026**

---

## 2. Présentations des membres

### Membre 1 (Chef de groupe)
* **Nom :** ADINSI-EGNONSE
* **Prénom :** Mahougnon Esther
* **École :** IFRI
* **Filière :** Génie Logiciel (GL)
* **Année :** L1
* **Téléphone :** 53675010
* **Email :** estheradinsi10@gmail.com

### Membre 2
* **Nom :** AKOMOTE
* **Prénom :** Akorédé Matinou
* **École :** IFRI
* **Filière :** Sécurité Informatique (SI)
* **Année :** L1
* **Téléphone :** 0199522784
* **Email :** akoredematinou322@gmail.com

### Membre 3
* **Nom :** ASSOGBA
* **Prénom :** Sheila Ayath
* **École :** IFRI
* **Filière :** Génie Logiciel (GL)
* **Année :** L1
* **Téléphone :** 0140649891
* **Email :** aliesbochi@gmail.com

### Membre 4
* **Nom :** BOCO
* **Prénom :** Tchégnidé Bertrand
* **École :** IFRI
* **Filière :** Intelligence Artificielle (IA)
* **Année :** L1
* **Téléphone :** 0140865724
* **Email :** bocobertrand89@gmail.com

### Membre 5
* **Nom :** BONOU
* **Prénom :** Gad Ezéckiel Jésulolo
* **École :** IFRI
* **Filière :** Sécurité Informatique (SI)
* **Année :** L1
* **Téléphone :** 0141868817
* **Email :** ezeckielbonou707@gmail.com

### Membre 6
* **Nom :** HOUNSA
* **Prénom :** Mahugnon Auriel Espoir Joram
* **École :** IFRI
* **Filière :** Sécurité Informatique (SI)
* **Année :** L1
* **Téléphone :** 0196389258
* **Email :** aurielhounsa4@gmail.com

### Membre 7
* **Nom :** LAMINOU
* **Prénom :** Fathi Adechinan
* **École :** IFRI
* **Filière :** Génie Logiciel (GL)
* **Année :** L1
* **Téléphone :** 01996091340
* **Email :** laminoufathiade@gmail.com

---

## 3. PROBLÈME IDENTIFIÉ
Au Bénin, les étudiants de l'IFRI éprouvent des difficultés à trouver un mentorat académique et professionnel efficace. Les causes principales sont :
* **Absence de plateforme centralisée :** Il n'existe pas de plateforme unique où les étudiants peuvent accéder directement aux mentors potentiels et aux offres de mentorat.
* **Manque d'outils adaptés :** Les étudiants ne disposent pas de modèles de profils ou de guides pour se présenter efficacement aux mentors. Il n'existe pas de ressources standardisées pour faciliter la mise en relation.
* **Dispersion des offres :** Les opportunités de mentorat sont publiées sur différents canaux (réseaux sociaux, bouche-à-oreille, sites génériques) sans centralisation, rendant difficile leur découverte.
* **Forte concurrence :** Dans certaines filières, les places de mentorat sont limitées et les étudiants ne savent pas comment se démarquer ou comment accéder aux mentors les plus pertinents.

---

## 4. DESCRIPTION DE LA SOLUTION
* **Nom de la solution :** IFRI_MentorLink
* **Description :** IFRI_MentorLink est une plateforme web qui centralise les offres de mentorat vérifiées et met en relation directe les étudiants de l'IFRI avec des mentors académiques et professionnels. Elle offre aux étudiants un accès simplifié aux opportunités de mentorat et met à leur disposition une boîte à outils complète (profils structurés, guides d'approche, messagerie intégrée) pour maximiser leurs chances de réussite. Les mentors, quant à eux, peuvent publier leurs offres et gérer les candidatures via un tableau de bord intuitif.

---

## 5. Exigences fonctionnelles

### Module public
* Page d'accueil avec présentation, avantages, statistiques et carrousel d'entreprises partenaires.
* Barre de recherche simple (filière, ville) pour explorer les offres.
* Modale de connexion/inscription avec choix du profil (étudiant/entreprise).

### Module authentification
* Inscription progressive avec barre de progression (étudiant : nom, prénom, email, téléphone, université, filière, niveau, mot de passe ; entreprise : nom, RCCM, email, adresse, description, logo, mot de passe).
* Validation des emails via lien de confirmation.
* Connexion sécurisée (email + mot de passe).
* Réinitialisation du mot de passe (via email).

### Dashboard étudiant
* **Vue d'ensemble :** indicateurs (candidatures envoyées, réponses, en attente), complétude du profil.
* **Recherche avancée :** avec filtres (filière, ville, type de demande, durée).
* **Liste des offres :** avec possibilité de postuler (simulation).
* **Gestion des candidatures :** suivi du statut (en attente, retenue, refusée), historique.
* **Profil étudiant :** modification des informations, upload de CV et lettre de motivation (PDF, photo).
* **Boîte à outils :** accès aux modèles de CV, lettres, guides d'entretien, checklists.

### Dashboard entreprise / Mentor
* **Vue d'ensemble :** indicateurs (offres publiées, candidatures reçues, réponses envoyées).
* **Gestion des offres :** créer, modifier, supprimer une offre de mentorat.
* **Gestion des candidatures :** consulter les candidatures, envoyer des réponses (acceptation, refus), ajouter des commentaires.

---

## 6. Technologies utilisées
* **Frontend :** HTML5, CSS3, JavaScript (vanilla)
* **Frameworks et bibliothèques :** Django (Backend Python)
* **Backend (phase 2) :** Python avec Django
* **Sécurité :** HTTPS, validation des données côté client et serveur

---

## 7. MODÈLE ÉCONOMIQUE
IFRI_MentorLink est une plateforme gratuite, conçue et gérée par des professionnels de l'éducation. Aucun modèle économique commercial n'est envisagé pour cette version initiale.

---

## 8. Perspectives et évolutions futures
* Intégration d'un système de notation et d'avis des mentors.
* Fonctionnalité de mentorat en groupe.
* Intégration avec les réseaux sociaux professionnels (LinkedIn).

---

## 9. Architecture et faisabilité technique

### Architecture générale
IFRI_MentorLink adopte une architecture client-serveur :
* **Client (Frontend) :** Interface web développée en HTML5, CSS3 et JavaScript.
* **Serveur (Backend) :** Logique métier implémentée en Python avec le framework Django.
* **Base de données :** Système de gestion de base de données relationnel (SGBDR) compatible SQL.