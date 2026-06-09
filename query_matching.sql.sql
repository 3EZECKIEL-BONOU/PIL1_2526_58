SELECT 
m.id AS mentor_id,
m.nom AS mentor_nom, 
m.prenom AS mentor_prenom,
mat.nom_matiere AS matiere_commune
(
	CASE WHEN m.filiere = u.filiere THEN 30 ELSE 0 END +  
	CASE WHEN m.niveau_etudes > u.niveau_etudes THEN 20 ELSE 0 END +
	(SELECT COUNT(*) * 10 FROM utilisateur_disponibilites ud1 
	JOIN utilisateur_disponibilites ud2 ON ud1.creneau_id = ud2.creneau_id
	WHERE ud1.utilisateur_id = u.id AND ud2.utilisateur_id = m.id)
) AS score_comptabilite
FROM utilisateurs u
JOIN utilisateur_lacunes ul ON u.id = ul.utilisateur_id
JOIN utilisateur_competences uc ON ul.matiere_id = uc.matiere_id
JOIN utilisateurs m ON uc.utilisateur_id = m.id
JOIN matieres mat ON ul.matiere_id = mat.id
WHERE u.id = 3
ORDER BY score_comptabilite DESC;