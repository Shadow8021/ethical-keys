#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
main.py - 
Démarre l'enregistrement automatiquement (pratique pour tests rapides).
Enregistre uniquement les frappes faites dans la Text widget (pas de hook global).
"""

import tkinter as tk
from datetime import datetime
import os
import sys

LOG_FILE = "local_keyrecorder_edu.log"
MAGIC_TAG = "LOCAL_KEYRECORDER_EDU_v1"

def now_iso():
    """Timestamp UTC ISO (utile pour trier/visualiser)."""
    return datetime.utcnow().isoformat(timespec="seconds") + "Z"

class AutoRecorderApp:
    def __init__(self, root):
        self.root = root
        root.title("Recorder pédagogique (auto) - corrigé")
        root.geometry("700x480")

        # Info simple pour l'utilisateur
        info = tk.Label(root, text=(
            "Cette version démarre l'enregistrement automatiquement.\n"
            "Clique dans la zone ci-dessous puis tape pour que les frappes soient enregistrées."
        ))
        info.pack(anchor="w", padx=10, pady=(8,0))

        # Zone de texte : seules les frappes ici sont captées
        self.text_area = tk.Text(root, wrap="word", height=22)
        self.text_area.pack(fill="both", expand=True, padx=10, pady=(6,8))
        self.text_area.insert("1.0", "Clique ici, puis tape. Le log est mis à jour et imprimé en console.\n")

        # état d'enregistrement
        self.recording = False

        # préparer fichier + tag (si absent)
        try:
            if not os.path.exists(LOG_FILE):
                with open(LOG_FILE, "w", encoding="utf-8") as f:
                    f.write(MAGIC_TAG + "\n")
            else:
                # garantir la présence du tag en début de fichier pour le TP YARA
                with open(LOG_FILE, "r+", encoding="utf-8") as f:
                    content = f.read()
                    if MAGIC_TAG not in content:
                        f.seek(0, 0)
                        f.write(MAGIC_TAG + "\n" + content)
        except Exception as e:
            print("Erreur lors de la préparation du fichier de log :", e, file=sys.stderr)

        # démarrer automatiquement l'enregistrement
        self.start_recording()

    def start_recording(self):
        """Lie l'événement Key à la Text widget et marque le début dans le log."""
        if not self.recording:
            self.text_area.bind("<Key>", self.on_key)
            self.recording = True
            self._log_local(f"--- AUTO START {now_iso()} ---\n")
            print("Enregistrement démarré (auto). Clique dans la zone de texte et tape.")

    def _log_local(self, text):
        """
        Fonction utilitaire pour écrire dans le fichier log ET afficher
        en console. On garde tout simple pour le TP.
        """
        # écriture sur disque (append)
        try:
            with open(LOG_FILE, "a", encoding="utf-8") as f:
                f.write(text)
        except Exception as e:
            print("Erreur écriture log:", e, file=sys.stderr)
        # echo console (pratique pour debug)
        print(text, end="")

    def on_key(self, event):
        """
        Handler appelé pour chaque Key press dans la Text widget.
        - event.char : le caractère imprimable (sinon '')
        - event.keysym : nom lisible de la touche
        """
        ts = now_iso()
        ch = event.char if event.char and event.char.isprintable() else ''
        if ch:
            line = f"{ts}\tCHAR\t'{ch}'\tkeysym={event.keysym}\n"
        else:
            line = f"{ts}\tNONCHAR\tkeysym={event.keysym}\n"
        # utilisation de la méthode commune pour log + console
        self._log_local(line)

if __name__ == "__main__":
    root = tk.Tk()
    app = AutoRecorderApp(root)
    root.mainloop()

