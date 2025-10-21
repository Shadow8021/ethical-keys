# Backlog Kanban — ethical-keys
Projet pédagogique d'apprentissage Python autour de la capture locale et éthique de frappes clavier dans une application console.

## Objectif général
Apprendre à structurer un projet Python collaboratif en suivant une approche par étapes :
- architecture claire
- code lisible et commenté
- capture locale et explicite des frappes clavier
- stockage, anonymisation, chiffrement et analyse de base
- respect du consentement utilisateur

---

## ETAPE 1 — Mise en place du projet
Objectif : disposer d’un squelette de projet exécutable par tous les membres.

### 1.1 – Créer la structure du projet
**But :** permettre à tous de lancer un programme commun.

À faire :
- Créer un dossier `ethical-keys/`
- Créer un sous-dossier `src/`
- Créer `src/main.py`
- Ajouter un `.gitignore` pour Python
- Écrire dans `src/main.py` :
  ```python
  print("Ethical Keys - Démarrage du projet")
  ```

Objectif atteint si le message s’affiche avec :
```bash
python src/main.py
```

---

### 1.2 – Créer un environnement virtuel
**But :** isoler les dépendances.

À faire :
```bash
python -m venv .venv
source .venv/bin/activate
```

Créer un fichier `requirements.txt` avec :
```
pydantic
```

Installer :
```bash
pip install -r requirements.txt
```

---

### 1.3 – Ajouter un README de base
**But :** décrire le but du projet et comment le lancer.

Contenu minimal :
```markdown
# Ethical Keys
Projet éducatif en Python : apprentissage des bases de la collecte locale d’événements clavier, dans un cadre éthique.
```

---

## ETAPE 2 — Capture locale en console
Objectif : afficher les touches tapées dans la console sans interface graphique.

### 2.1 – Lecture clavier en console
**But :** intercepter les frappes utilisateur sans quitter le terminal.

À faire :
- Créer `src/telemetry/input_reader.py`
- Utiliser la bibliothèque standard `keyboard` ou `pynput`
- Exemple de structure :
  ```python
  import keyboard

  def start_capture():
      print("Appuyez sur 'ESC' pour arrêter.")
      while True:
          event = keyboard.read_event()
          if event.name == "esc":
              break
          if event.event_type == "down":
              print(f"Touche: {event.name}")
  ```

---

### 2.2 – Lancer la capture depuis main.py
**But :** permettre à l’utilisateur de démarrer la capture depuis la console.

À faire dans `main.py` :
```python
from telemetry.input_reader import start_capture

if __name__ == "__main__":
    start_capture()
```

Objectif atteint si :
- Les frappes apparaissent dans le terminal.
- Le programme s’arrête avec la touche ESC.

---

## ETAPE 3 — Enregistrement des frappes
Objectif : sauvegarder les touches tapées dans un fichier texte.

### 3.1 – Créer un module collector
**But :** écrire les frappes dans un fichier local.

À faire :
Créer `src/telemetry/collector.py`
```python
from datetime import datetime

def save_key(key):
    with open("keys.log", "a") as f:
        f.write(f"{datetime.now()} - {key}\n")
```

---

### 3.2 – Appeler le collector depuis input_reader
**But :** enregistrer les frappes au fur et à mesure.

```python
from telemetry.collector import save_key

def start_capture():
    import keyboard
    print("Appuyez sur ESC pour arrêter.")
    while True:
        event = keyboard.read_event()
        if event.name == "esc":
            break
        if event.event_type == "down":
            save_key(event.name)
```

Objectif atteint si un fichier `keys.log` est créé et contient les touches tapées.

---

## ETAPE 4 — Structure du projet et modèles
Objectif : organiser le code pour que chacun puisse travailler sur une partie spécifique.

### 4.1 – Créer les modules de base
Créer les fichiers suivants dans `src/telemetry/` :
- `domain.py`
- `collector.py`
- `sanitizer.py`
- `crypto.py`
- `storage.py`
- `analysis.py`

Tous peuvent être vides au départ.

---

### 4.2 – Créer la classe InputEvent
**But :** représenter chaque frappe sous forme d’objet.

```python
from datetime import datetime
from pydantic import BaseModel

class InputEvent(BaseModel):
    key: str
    timestamp: datetime
```

---

## ETAPE 5 — Anonymisation et sécurité
Objectif : masquer les données sensibles avant la sauvegarde.

### 5.1 – Masquage basique
Créer `sanitizer.py`
```python
import re

def sanitize(text):
    text = re.sub(r"\S+@\S+", "[EMAIL]", text)
    text = re.sub(r"\d{4,}", "[NUM]", text)
    return text
```

Modifier `collector.py` :
```python
from telemetry.sanitizer import sanitize

def save_key(key):
    key = sanitize(key)
    ...
```

---

### 5.2 – Chiffrement des données
Créer `crypto.py`
```python
from cryptography.fernet import Fernet

key = Fernet.generate_key()
cipher = Fernet(key)

def encrypt(text):
    return cipher.encrypt(text.encode()).decode()

def decrypt(token):
    return cipher.decrypt(token.encode()).decode()
```

Modifier `collector.py` pour chiffrer avant sauvegarde.

---

## ETAPE 6 — Analyse des données
Objectif : calculer quelques statistiques à partir du fichier des frappes.

### 6.1 – Compter le nombre de frappes
Créer `analysis.py`
```python
def count_keys(filename="keys.log"):
    with open(filename) as f:
        return len(f.readlines())
```

### 6.2 – Calcul du temps moyen entre deux frappes
Lire le fichier, extraire les timestamps, et calculer la moyenne des écarts.

---

## ETAPE 7 — Aspects éthiques et documentation
Objectif : comprendre et documenter les limites du projet.

### 7.1 – Créer la charte éthique
Fichier `ETHICS.md` :
```markdown
# Charte éthique
- Les frappes sont captées uniquement dans la console locale.
- Aucune donnée personnelle ni système n’est collectée.
- Tout reste local, aucune transmission externe.
- L’utilisateur peut effacer le fichier keys.log à tout moment.
```

### 7.2 – Ajouter un script de suppression des données
Créer `src/telemetry/clear_data.py`
```python
def clear_log():
    open("keys.log", "w").close()
    print("Données effacées.")
```

---

## ETAPE 8 — Collaboration et bonnes pratiques
Objectif : apprendre à travailler à plusieurs sur GitHub.

### 8.1 – Branches de développement
Règle simple :
- Une fonctionnalité = une branche
- Toujours faire une pull request avant de merger

### 8.2 – Convention de commits
Forme recommandée :
```
feat: ajout du module collector
fix: correction du bug d’écriture
docs: mise à jour du README
```

---

## ETAPE 9 — Bonus possibles
Objectif : aller plus loin une fois les bases acquises.

Idées :
- Sauvegarde dans une base SQLite au lieu d’un fichier
- Ajout d’un système de logs chiffrés par session
- Création d’un script d’analyse (classement des touches les plus tapées)
- Génération d’un rapport en CSV

---

## ETAPE 10 — Validation finale
Objectif : prouver que le projet fonctionne et que tout le monde comprend chaque partie.

Checklist de fin :
- [ ] La capture fonctionne
- [ ] Les frappes sont stockées localement
- [ ] Les données sont masquées
- [ ] Le chiffrement fonctionne
- [ ] Le projet est documenté
- [ ] Chacun peut expliquer sa partie
