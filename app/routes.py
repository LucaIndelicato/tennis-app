from flask import Blueprint, render_template, flash, redirect, url_for, request
from app import db
from app.forms import RegistrationForm, LoginForm, QuizForm, EventForm
from app.models import User, Event
from flask_login import current_user, login_user, logout_user, login_required
from datetime import datetime, date 

bp = Blueprint('main', __name__)

################################################## INDEX PART ##################################################
@bp.route('/')
@bp.route('/index')
@login_required
def index():
    # Query per trovare tutti gli eventi futuri
    today = date.today()
    events = Event.query.filter(Event.data_ora >= today).order_by(Event.data_ora.asc()).all()

    # --- NUOVA LOGICA: CALCOLO STATISTICHE UTENTE ---
    eventi_partecipati = current_user.eventi_iscritti.count()
    eventi_creati = Event.query.filter_by(creatore=current_user).count()
    
    return render_template(
        'index.html', 
        title='Bacheca', 
        events=events,
        eventi_partecipati=eventi_partecipati,
        eventi_creati=eventi_creati
    )

################################################## EVENTS PART ##################################################
@bp.route('/create_event', methods=['GET', 'POST'])
@login_required
def create_event():
    form = EventForm()
    if form.validate_on_submit():
        event = Event(
            titolo=form.titolo.data,
            tipologia=form.tipologia.data,
            descrizione=form.descrizione.data,
            data_ora=form.data_ora.data,
            luogo=form.luogo.data,
            max_partecipanti=form.max_partecipanti.data,
            livello_consigliato=form.livello_consigliato.data,
            creatore=current_user
        )
        # Aggiungiamo automaticamente il creatore come primo partecipante
        event.iscritti.append(current_user)
        db.session.add(event)
        db.session.commit()
        flash('Il tuo evento è stato creato!', 'success')
        return redirect(url_for('main.index'))
    return render_template('create_event.html', title='Crea Evento', form=form)


@bp.route('/join_event/<int:event_id>', methods=['POST'])
@login_required
def join_event(event_id):
    event = Event.query.get_or_404(event_id)
    if event.iscritti.count() >= event.max_partecipanti:
        flash('Questo evento è al completo!', 'error')
    elif current_user in event.iscritti:
        flash('Sei già iscritto a questo evento.', 'info')
    else:
        event.iscritti.append(current_user)
        db.session.commit()
        flash('Ti sei iscritto all\'evento con successo!', 'success')
    return redirect(url_for('main.index'))

@bp.route('/leave_event/<int:event_id>', methods=['POST'])
@login_required
def leave_event(event_id):
    event = Event.query.get_or_404(event_id)
    if current_user in event.iscritti:
        event.iscritti.remove(current_user)
        db.session.commit()
        flash('Hai annullato la tua iscrizione all\'evento.', 'success')
    else:
        flash('Non sei iscritto a questo evento.', 'error')
    return redirect(url_for('main.index'))

################################################## LOGIN/REGISTER PART ##################################################
@bp.route('/login', methods=['GET', 'POST'])
def login():
    # Se l'utente è già loggato, lo mandiamo alla homepage
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        # Cerca l'utente nel database tramite la sua email
        user = User.query.filter_by(email=form.email.data).first()
        
        # Se l'utente non esiste o la password è sbagliata, mostra un errore
        if user is None or not user.check_password(form.password.data):
            flash('Email o password non validi', 'error')
            return redirect(url_for('main.login'))
        
        # Se i dati sono corretti, effettua il login
        login_user(user, remember=form.remember_me.data)
        flash(f'Accesso effettuato come {user.nome}!', 'success')
        
        # Reindirizza alla pagina che l'utente stava cercando di visitare, o alla homepage
        next_page = request.args.get('next')
        if not next_page:
            next_page = url_for('main.index')
        return redirect(next_page)
        
    return render_template('login.html', title='Login', form=form)

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            nome=form.nome.data,
            email=form.email.data,
            cap=form.cap.data
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        
        flash('Congratulazioni, la registrazione è avvenuta con successo!', 'success')
        return redirect(url_for('main.login'))
        
    return render_template('register.html', title='Registrazione', form=form)


################################################## QUIZ PART ##################################################
@bp.route('/quiz', methods=['GET', 'POST'])
@login_required
def quiz():
    form = QuizForm()
    if form.validate_on_submit():
        score = 0
        # Calcola il punteggio sommando i valori delle risposte (che sono stringhe '1', '2', '3')
        score += float(form.q0.data)
        score += float(form.q1.data)
        score += float(form.q2.data)
        score += float(form.q3.data)
        score += float(form.q4.data)
        score += float(form.q5.data)
        score += float(form.q6.data)
        score += float(form.q7.data)
        score += float(form.q8.data)
        score += float(form.q9.data)
        score += float(form.q10.data)

        # Determina il livello in base al punteggio
        livello = ''
        if score <= 10:
            livello = 'Principiante'
        elif score <= 17:
            livello = 'Intermedio'
        else:
            livello = 'Avanzato'
        
        # Aggiorna il livello dell'utente corrente nel database
        current_user.livello = livello
        db.session.commit()
        
        flash(f'Quiz completato! Il tuo nuovo livello è: {livello}', 'success')
        return redirect(url_for('main.index'))

    return render_template('quiz.html', title='Quiz Livello', form=form)
