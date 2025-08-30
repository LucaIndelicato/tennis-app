import os

# Trova il percorso assoluto della directory del file corrente
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    """Configurazioni di base dell'applicazione."""
    # Chiave segreta per proteggere i form e le sessioni
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'una-chiave-segreta-molto-difficile-da-indovinare'
    WTF_CSRF_SECRET_KEY = "una-chiave-segreta-per-i-form"
    
    # Configurazione del database SQLite
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or \
        'sqlite:///' + os.path.join(basedir, 'instance', 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False