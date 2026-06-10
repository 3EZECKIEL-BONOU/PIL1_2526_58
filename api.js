/**
 * ============================================================
 *  IFRI MentorLink — Couche API
 *  Fichier : api.js
 *  Rôle    : Centralise tous les appels vers le backend Django
 * ============================================================
 */

const BASE_URL = 'http://localhost:8000';

// ══════════════════════════════════════════════════════════
//  GESTION DES TOKENS JWT
// ══════════════════════════════════════════════════════════

function getAccessToken()  { return localStorage.getItem('access_token');  }
function getRefreshToken() { return localStorage.getItem('refresh_token'); }

function saveTokens(access, refresh) {
  localStorage.setItem('access_token',  access);
  localStorage.setItem('refresh_token', refresh);
}

function clearTokens() {
  localStorage.removeItem('access_token');
  localStorage.removeItem('refresh_token');
}

/**
 * Rafraîchit le token d'accès avec le refresh token.
 * Retourne true si succès, false sinon.
 */
async function refreshAccessToken() {
  const refresh = getRefreshToken();
  if (!refresh) return false;

  try {
    const res = await fetch(`${BASE_URL}/api/token/refresh/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ refresh })
    });
    if (!res.ok) return false;

    const data = await res.json();
    localStorage.setItem('access_token', data.access);
    return true;
  } catch {
    return false;
  }
}

// ══════════════════════════════════════════════════════════
//  REQUÊTE DE BASE (avec gestion auto du token expiré)
// ══════════════════════════════════════════════════════════

/**
 * Effectue une requête authentifiée vers le backend.
 * Gère automatiquement le refresh JWT et la redirection si déconnecté.
 *
 * @param {string} endpoint  - ex: '/api/matching/'
 * @param {object} options   - options fetch (method, body, headers…)
 * @returns {object|null}    - données JSON ou null si erreur
 */
async function apiFetch(endpoint, options = {}) {
  const makeRequest = (token) =>
    fetch(BASE_URL + endpoint, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...(token ? { Authorization: `Bearer ${token}` } : {}),
        ...(options.headers || {})
      }
    });

  let res = await makeRequest(getAccessToken());

  // Token expiré → on tente un refresh
  if (res.status === 401) {
    const refreshed = await refreshAccessToken();
    if (refreshed) {
      res = await makeRequest(getAccessToken());
    } else {
      clearTokens();
      window.location.href = 'connexion_etudiant.html';
      return null;
    }
  }

  if (!res.ok) {
    console.error(`[API] Erreur ${res.status} sur ${endpoint}`);
    return null;
  }

  // Réponse vide (ex: 204 No Content)
  if (res.status === 204) return true;

  return res.json();
}

// ══════════════════════════════════════════════════════════
//  AUTHENTIFICATION
// ══════════════════════════════════════════════════════════

/**
 * Connecte l'utilisateur et stocke ses tokens.
 * @returns {boolean} succès ou échec
 */
async function login(email, password) {
  try {
    const res = await fetch(`${BASE_URL}/api/token/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password })
    });

    if (!res.ok) return false;

    const data = await res.json();
    saveTokens(data.access, data.refresh);
    return true;
  } catch {
    return false;
  }
}

function logout() {
  clearTokens();
  window.location.href = 'connexion_etudiant.html';
}

// ══════════════════════════════════════════════════════════
//  UTILISATEUR CONNECTÉ
// ══════════════════════════════════════════════════════════

/**
 * Récupère le profil de l'utilisateur connecté.
 */
async function fetchProfil() {
  return await apiFetch('/api/users/me/');
}

/**
 * Met à jour le profil de l'utilisateur connecté.
 */
async function updateProfil(data) {
  return await apiFetch('/api/users/me/', {
    method: 'PATCH',
    body: JSON.stringify(data)
  });
}

// ══════════════════════════════════════════════════════════
//  MATCHING — Recommandations de mentors
// ══════════════════════════════════════════════════════════

/**
 * Récupère la liste des mentors recommandés pour l'étudiant connecté.
 * Retourne { recommendations: [...] }
 */
async function fetchRecommandations() {
  return await apiFetch('/api/matching/');
}

/**
 * Récupère la liste des mentors déjà actifs (déjà contactés).
 */
async function fetchMesmentors() {
  return await apiFetch('/api/matching/mes-mentors/');
}

// ══════════════════════════════════════════════════════════
//  DEMANDES DE MENTORAT
// ══════════════════════════════════════════════════════════

/**
 * Récupère les demandes de l'étudiant connecté.
 */
async function fetchDemandes() {
  return await apiFetch('/api/matching/demandes/');
}

/**
 * Crée une nouvelle demande de mentorat.
 */
async function creerDemande({ matiere, description, format, disponibilite }) {
  return await apiFetch('/api/matching/demandes/', {
    method: 'POST',
    body: JSON.stringify({ matiere, description, format, disponibilite })
  });
}

/**
 * Clôture une demande existante.
 */
async function cloturerDemande(demandeId) {
  return await apiFetch(`/api/matching/demandes/${demandeId}/cloturer/`, {
    method: 'PATCH'
  });
}

// ══════════════════════════════════════════════════════════
//  MESSAGERIE
// ══════════════════════════════════════════════════════════

/**
 * Récupère toutes les conversations de l'étudiant connecté.
 */
async function fetchConversations() {
  return await apiFetch('/api/messaging/conversations/');
}

/**
 * Récupère les messages d'une conversation avec un mentor.
 */
async function fetchMessages(mentorId) {
  return await apiFetch(`/api/messaging/conversations/${mentorId}/messages/`);
}

/**
 * Envoie un message à un mentor.
 */
async function envoyerMessage(destinataireId, contenu) {
  return await apiFetch('/api/messaging/messages/', {
    method: 'POST',
    body: JSON.stringify({ destinataire_id: destinataireId, contenu })
  });
}

// ══════════════════════════════════════════════════════════
//  SESSIONS
// ══════════════════════════════════════════════════════════

/**
 * Récupère les sessions à venir de l'étudiant.
 */
async function fetchSessionsAVenir() {
  return await apiFetch('/api/matching/sessions/?statut=upcoming');
}

/**
 * Récupère les sessions passées de l'étudiant.
 */
async function fetchSessionsPassees() {
  return await apiFetch('/api/matching/sessions/?statut=done');
}

/**
 * Crée une demande de session avec un mentor.
 */
async function demanderSession({ mentorId, matiere, date, heure, format }) {
  return await apiFetch('/api/matching/sessions/', {
    method: 'POST',
    body: JSON.stringify({ mentor_id: mentorId, matiere, date, heure, format })
  });
}

/**
 * Annule une session.
 */
async function annulerSession(sessionId) {
  return await apiFetch(`/api/matching/sessions/${sessionId}/annuler/`, {
    method: 'PATCH'
  });
}

// ══════════════════════════════════════════════════════════
//  NOTIFICATIONS
// ══════════════════════════════════════════════════════════

/**
 * Récupère les notifications non lues.
 */
async function fetchNotifications() {
  return await apiFetch('/api/notifications/');
}

/**
 * Marque toutes les notifications comme lues.
 */
async function marquerNotificationsLues() {
  return await apiFetch('/api/notifications/marquer-lues/', { method: 'POST' });
}

// ══════════════════════════════════════════════════════════
//  UTILITAIRE — Formater un mentor brut (réponse API → state)
// ══════════════════════════════════════════════════════════

const COLORS = ['av-b', 'av-g', 'av-p', 'av-o'];

function formaterMentor(raw, index = 0) {
  const mentor = raw.mentor || raw;
  const offre  = raw.offre  || {};
  const prenom = mentor.prenom || '';
  const nom    = mentor.nom    || '';

  return {
    id       : mentor.id,
    initiales: `${prenom[0] || ''}${nom[0] || ''}`.toUpperCase(),
    color    : COLORS[index % COLORS.length],
    nom      : `${prenom} ${nom}`.trim(),
    filiere  : mentor.filiere        || '',
    niveau   : mentor.niveau_etudes  || '',
    chips    : offre.matiere ? [offre.matiere.nom] : (mentor.competences || []),
    score    : raw.score             || 0,
    dispo    : (raw.horaires_communs || []).join(', ') || 'À définir',
    format   : offre.format          || 'En ligne',
  };
}

function formaterSession(raw) {
  const d    = new Date(raw.date);
  const mois = ['Jan','Fév','Mar','Avr','Mai','Juin','Juil','Aoû','Sep','Oct','Nov','Déc'][d.getMonth()];
  return {
    id       : raw.id,
    matiere  : raw.matiere?.nom || raw.matiere || '',
    mentor   : raw.mentor_nom  || '',
    date     : `${d.getDate()} ${mois}`,
    dateShort: String(d.getDate()),
    mois,
    heure    : raw.heure || '',
    format   : raw.format || '',
    status   : raw.statut || 'En attente',
  };
}

function formaterDemande(raw) {
  const d = new Date(raw.date_creation);
  return {
    id      : raw.id,
    matiere : raw.matiere?.nom || raw.matiere || '',
    desc    : raw.description  || '',
    format  : raw.format       || '',
    dispo   : raw.disponibilite || 'Non précisé',
    date    : `${d.getDate()}/${d.getMonth() + 1}/${d.getFullYear()}`,
    status  : raw.statut === 'active' ? 'Active' : raw.statut === 'cloturee' ? 'Clôturée' : 'En attente',
    reponses: raw.nb_reponses  || 0,
  };
}
