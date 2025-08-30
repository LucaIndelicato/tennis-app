# app/__init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from config import Config
import os

# 1. Inizializza le estensioni QUI, fuori dalla funzione
db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()
login_manager.login_view = 'main.login'
login_manager.login_message = "Per favore, effettua il login per accedere a questa pagina."

def create_app(config_class=Config):
    """Factory function per creare l'istanza dell'app Flask."""
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Assicura che la cartella 'instance' esista
    instance_path = os.path.join(os.path.dirname(app.root_path), 'instance')
    os.makedirs(instance_path, exist_ok=True)

    # 2. Collega le estensioni all'app QUI
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    # 3. Sposta gli import che dipendono dall'app QUI DENTRO
    with app.app_context():
        from app import routes, models

        # Registra le rotte (routes)
        app.register_blueprint(routes.bp)
        
        @login_manager.user_loader
        def load_user(user_id):
            return models.User.query.get(int(user_id))

    return app