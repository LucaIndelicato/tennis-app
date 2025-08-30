import os
from app import create_app, db

# --- PARTE 1: CANCELLAZIONE DEL DATABASE ESISTENTE ---

# Definiamo il percorso del file del database
# Questo script deve trovarsi nella cartella principale del progetto (es. tennis-app/)
basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'instance', 'app.db')

print(f"Percorso del database: {db_path}")

# Controlliamo se il file del database esiste
if os.path.exists(db_path):
    try:
        # Se esiste, lo eliminiamo
        os.remove(db_path)
        print("Vecchio database eliminato con successo.")
    except OSError as e:
        print(f"Errore durante l'eliminazione del file: {e}")
else:
    print("Nessun database esistente da eliminare.")

print("Creazione di un nuovo database pulito...")
app = create_app()
with app.app_context():
    db.create_all()

exit()