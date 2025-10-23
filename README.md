# Ethical Keys

Petit projet éducatif pour apprendre les bases de la capture d’événements clavier en Python, dans un contexte éthique et contrôlé.  
Ce projet s’inscrit dans une formation en cybersécurité où l’objectif est d’observer, comprendre et détecter le comportement d’un keylogger, sans jamais en développer un malveillant.

---

## Objectifs pédagogiques

- Comprendre les principes de base d’un enregistreur de touches dans une fenêtre Python (événements clavier, timestamp, enregistrement local).  
- Étudier les bonnes pratiques éthiques et les limitations légales (aucune capture système ni dissimulation).  
- Créer une signature YARA pour détecter la présence du programme ou de ses fichiers de log.  
- Apprendre à reconnaître les patterns typiques des malwares de type keylogger dans un environnement sécurisé.

---

## Fonctionnement

Le script `main.py` ouvre une fenêtre graphique (Tkinter) et enregistre uniquement les touches tapées dans la zone de texte de cette fenêtre.

Les frappes sont :
- affichées dans la console en temps réel,
- écrites dans un fichier local `/tmp/local_keyrecorder_edu.log`,
- horodatées en UTC,
- précédées d’un tag unique `LOCAL_KEYRECORDER_EDU_v1` (utile pour l’analyse YARA).

Aucune capture globale du système, ni en arrière-plan.

---

## Utilisation

### 1. Lancer le programme
```bash
python3 main.py
```

Une fenêtre s’ouvre automatiquement (au premier plan).  
Clique dans la zone de texte et tape : tes frappes seront enregistrées localement.

### 2. Suivre le log en temps réel
```bash
tail -f /tmp/local_keyrecorder_edu.log
```

### 3. Arrêter le programme
Ferme simplement la fenêtre ou fais `Ctrl+C` dans le terminal.

---

## Exemple de log

```
LOCAL_KEYRECORDER_EDU_v1
--- AUTO START 2025-10-23T18:49:45Z ---
2025-10-23T18:50:01Z    CHAR    'a'    keysym=a
2025-10-23T18:50:02Z    CHAR    'b'    keysym=b
2025-10-23T18:50:03Z    NONCHAR keysym=Return
```

---

## Structure du projet

```
ethical-keys/
├── main.py                      # Script principal (interface Tkinter)
├── /tmp/local_keyrecorder_edu.log   # Fichier de log généré (non versionné)
├── server.py                    # Placeholder (future extension réseau)
├── src/                         # Dossier source (tests, modules futurs)
└── README.md                    # Ce fichier
```

---

## Aspects éthiques et légaux

Ce code ne doit jamais être modifié pour capturer des frappes hors du cadre de la fenêtre ou pour être utilisé sans consentement explicite.  
Il est destiné à un usage strictement pédagogique dans un environnement de test isolé (VM).  
L’analyse via YARA fait partie de l’exercice pour apprendre à détecter ces comportements.

---

## Exemple de règle YARA (détection du tag)

```yara
rule edu_local_keyrecorder
{
    meta:
        author = "Étudiant en cybersécurité"
        description = "Détection du keylogger éducatif ethical-keys"
        date = "2025-10-23"

    strings:
        $tag = "LOCAL_KEYRECORDER_EDU_v1"

    condition:
        $tag
}
```

---

## Prérequis techniques

- Python 3.10 ou supérieur  
- Tkinter (inclus par défaut dans Python.org, ou via `brew install tcl-tk` sur macOS)  
- macOS, Linux ou Windows (testé sur macOS 14)

---

## Auteur

Projet réalisé par Clémence Chopin dans le cadre d’une formation en cybersécurité.  
Objectif : apprentissage du Python appliqué à la sécurité offensive et défensive (concepts de keylogging, détection YARA, etc.).

