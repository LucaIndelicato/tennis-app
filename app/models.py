from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

partecipanti = db.Table('partecipanti',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('event_id', db.Integer, db.ForeignKey('event.id'), primary_key=True)
)
# collega l'ID di chi segue (follower_id) a chi è seguito (followed_id).
rally = db.Table('rally',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'), primary_key=True)
)

class User(UserMixin, db.Model):
    """Modello per la tabella degli utenti."""
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(64), index=True, nullable=False)
    cognome = db.Column(db.String(64), index=True, nullable=True)
    data_di_nascita = db.Column(db.Date, nullable=True)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    cap = db.Column(db.String(5), nullable=False)
    password_hash = db.Column(db.String(256))
    livello = db.Column(db.String(20), default='Principiante')
    # Definiamo la relazione che ci permette di vedere con chi stiamo facendo rally.
    # 'followed' rappresenta la lista degli utenti che l'utente corrente sta seguendo.
    followed = db.relationship(
        'User', secondary=rally,
        primaryjoin=(rally.c.follower_id == id),
        secondaryjoin=(rally.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'), 
        lazy='dynamic'
    )

    # 3. AGGIUNGIAMO DEI METODI HELPER PER SEMPLICITA'
    # Questi metodi nascondono la complessità della gestione del database
    # e ci permetteranno di scrivere codice più pulito nelle nostre routes.
    
    def start_rally(self, user):
        """Aggiunge un utente alla lista di quelli con cui facciamo rally."""
        if not self.is_rallying(user):
            self.followed.append(user)

    def stop_rally(self, user):
        """Rimuove un utente dalla lista di quelli con cui facciamo rally."""
        if self.is_rallying(user):
            self.followed.remove(user)

    def is_rallying(self, user):
        """Controlla se stiamo già facendo rally con un determinato utente."""
        return self.followed.filter(
            rally.c.followed_id == user.id).count() > 0
    
    def set_password(self, password):
        """Crea un hash sicuro della password."""
        # Specifichiamo il metodo di hashing per massima compatibilità
        self.password_hash = generate_password_hash(password, method='pbkdf2:sha256')
    
    def check_password(self, password):
        """Verifica se la password fornita corrisponde all'hash salvato."""
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.nome}>'

class Event(db.Model):
    """Modello per la tabella degli eventi."""
        # --- LISTE CENTRALIZZATE ---
    TIPOLOGIA_CHOICES = [
        ('Partita 1vs1', 'Partita 1vs1'),
        ('Partita 2vs2', 'Partita 2vs2'),
        ('Allenamento guidato', 'Allenamento guidato'),
        ('Lezione', 'Lezione')
    ]
    LIVELLO_CHOICES = [
        ('Principiante', 'Principiante'),
        ('Intermedio', 'Intermedio'),
        ('Avanzato', 'Avanzato'),
        ('Tutti', 'Tutti i livelli')
    ]
    # --- FINE LISTE ---
    id = db.Column(db.Integer, primary_key=True)
    titolo = db.Column(db.String(100), nullable=False)
    tipologia = db.Column(db.String(50), nullable=False)
    descrizione = db.Column(db.String(10000))
    data_ora = db.Column(db.DateTime, nullable=False, index=True)
    # durata = db.Column(db.Integer, nullable=False )
    luogo = db.Column(db.String(100), nullable=False)
    max_partecipanti = db.Column(db.Integer, nullable=False)
    livello_consigliato = db.Column(db.String(20), nullable=False)
    
    # Chiave esterna per collegare l'evento al suo creatore
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    creatore = db.relationship('User')

    # Relazione Molti-a-Molti con gli utenti che partecipano
    iscritti = db.relationship(
        'User', secondary=partecipanti,
        backref=db.backref('eventi_iscritti', lazy='dynamic'),
        lazy='dynamic')

    def __repr__(self):
        return f'<Event {self.tipologia} a {self.luogo}>'
