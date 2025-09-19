from flask import Blueprint, render_template, flash, redirect, url_for, request, abort
from app import db
from app.forms import *
from app.models import *
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

# ==============================================================================
# PAGINA DEDICATA A TUTTI GLI EVENTI CON FILTRI
# ==============================================================================
@bp.route('/events', methods=['GET', 'POST'])
@login_required
def events():
    form = EventFilterForm(request.form)
    # --- NUOVA LOGICA: POPOLIAMO LA DROPDOWN DEI CREATORI ---
    # 1. Troviamo gli ID di tutti gli utenti che sono creatori di almeno un evento
    creator_ids = db.session.query(Event.user_id).distinct().all()
    # 2. Trasformiamo la lista di tuple in una lista semplice di ID
    creator_ids_list = [c[0] for c in creator_ids]
    # 3. Recuperiamo gli oggetti User completi
    creators = User.query.filter(User.id.in_(creator_ids_list)).order_by(User.nome).all()
    # 4. Assegnamo le choices al campo del form
    form.creatore.choices = [('', 'Tutti i creatori')] + [(str(u.id), u.nome) for u in creators]
    # --- FINE NUOVA LOGICA ---


    # Partiamo da una query di base: tutti gli eventi futuri, ordinati per data
    query = Event.query.filter(Event.data_ora >= date.today()).order_by(Event.data_ora.asc())

    # Applichiamo i filtri solo se il form viene inviato con metodo POST
    if request.method == 'POST' and form.validate():
        
        # Filtro 1: Ricerca testuale per titolo o luogo
        if form.query.data:
            search_term = f"%{form.query.data}%"
            # Usiamo db.or_ per cercare il termine in entrambe le colonne
            query = query.filter(db.or_(Event.titolo.ilike(search_term), Event.luogo.ilike(search_term)))
        
        # Filtro 2: Data esatta
        if form.data.data:
            # Filtriamo per la parte "data" del campo data_ora
            query = query.filter(db.func.date(Event.data_ora) == form.data.data)

        # Filtro 3: Tipologia esatta
        if form.tipologia.data:
            query = query.filter(Event.tipologia == form.tipologia.data)
            
        # Filtro 4: Nome del creatore
        if form.creatore.data:
            query = query.filter(Event.user_id == form.creatore.data)

    # Eseguiamo la query finale (filtrata o non) per ottenere la lista degli eventi
    all_events = query.all()
    
    return render_template('events.html', title='Tutti gli Eventi', form=form, events=all_events)

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

@bp.route('/edit_event/<int:event_id>', methods=['GET', 'POST'])
@login_required
def edit_event(event_id):
    event = Event.query.get_or_404(event_id)
    # Controllo di sicurezza: solo il creatore può modificare
    if event.creatore != current_user:
        abort(403) # Forbidden
        
    form = EventForm()
    if form.validate_on_submit():
        # Aggiorna i dati dell'evento con quelli del form
        event.titolo = form.titolo.data
        event.tipologia = form.tipologia.data
        event.descrizione = form.descrizione.data
        event.data_ora = form.data_ora.data
        event.luogo = form.luogo.data
        event.max_partecipanti = form.max_partecipanti.data
        event.livello_consigliato = form.livello_consigliato.data
        db.session.commit()
        flash('Il tuo evento è stato aggiornato!', 'success')
        return redirect(url_for('main.index'))
    elif request.method == 'GET':
        # Pre-compila il form con i dati esistenti dell'evento
        form.titolo.data = event.titolo
        form.tipologia.data = event.tipologia
        form.descrizione.data = event.descrizione
        form.data_ora.data = event.data_ora
        form.luogo.data = event.luogo
        form.max_partecipanti.data = event.max_partecipanti
        form.livello_consigliato.data = event.livello_consigliato
        
    return render_template('edit_event.html', title='Modifica Evento', form=form, event=event)


@bp.route('/delete_event/<int:event_id>', methods=['POST'])
@login_required
def delete_event(event_id):
    event = Event.query.get_or_404(event_id)
    # Controllo di sicurezza: solo il creatore può eliminare
    if event.creatore != current_user:
        abort(403)
        
    db.session.delete(event)
    db.session.commit()
    flash('L\'evento è stato cancellato con successo.', 'success')
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

################################################## ACCOUNT PART ##################################################
@bp.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    
    # Se l'utente sta inviando il form (POST)
    if form.validate_on_submit():
        current_user.nome = form.nome.data
        current_user.cognome = form.cognome.data
        current_user.data_di_nascita = form.data_di_nascita.data
        db.session.commit()
        flash('Il tuo profilo è stato aggiornato!', 'success')
        return redirect(url_for('main.account'))
    
    # Se l'utente sta solo visitando la pagina (GET)
    elif request.method == 'GET':
        form.nome.data = current_user.nome
        form.cognome.data = current_user.cognome
        form.data_di_nascita.data = current_user.data_di_nascita

    # Calcoliamo le statistiche (logica già presente in index)
    eventi_partecipati = current_user.eventi_iscritti.count()
    eventi_creati = Event.query.filter_by(creatore=current_user).count()

    # Calcoliamo l'età
    eta = None
    if current_user.data_di_nascita:
        today = date.today()
        eta = today.year - current_user.data_di_nascita.year - ((today.month, today.day) < (current_user.data_di_nascita.month, current_user.data_di_nascita.day))

    return render_template(
        'account.html', 
        title='Il Tuo Profilo', 
        form=form,
        eventi_partecipati=eventi_partecipati,
        eventi_creati=eventi_creati,
        eta=eta
    )

# ==============================================================================
# SEZIONE PER LA GESTIONE DEI RALLY (FOLLOW/UNFOLLOW)
# ==============================================================================

@bp.route('/rally/<username>', methods=['POST'])
@login_required
def rally_user(username):
    """Route per iniziare a fare rally con un utente."""
    user_to_follow = User.query.filter_by(nome=username).first()
    
    # Controlli di sicurezza
    if user_to_follow is None:
        flash(f'Utente {username} non trovato.', 'error')
        return redirect(url_for('main.index'))
    if user_to_follow == current_user:
        flash('Non puoi fare rally con te stesso!', 'warning')
        return redirect(url_for('main.index'))
        
    # Usiamo il nostro metodo helper per iniziare il rally
    current_user.start_rally(user_to_follow)
    db.session.commit()
    flash(f'Hai iniziato un rally con {username}!', 'success')
    
    # Reindirizza l'utente alla pagina da cui proveniva
    return redirect(request.referrer or url_for('main.index'))


@bp.route('/unrally/<username>', methods=['POST'])
@login_required
def unrally_user(username):
    """Route per smettere di fare rally con un utente."""
    user_to_unfollow = User.query.filter_by(nome=username).first()
    
    # Controlli di sicurezza
    if user_to_unfollow is None:
        flash(f'Utente {username} non trovato.', 'error')
        return redirect(url_for('main.index'))
    if user_to_unfollow == current_user:
        flash('Non puoi smettere di fare rally con te stesso.', 'warning')
        return redirect(url_for('main.index'))
        
    # Usiamo il nostro metodo helper per terminare il rally
    current_user.stop_rally(user_to_unfollow)
    db.session.commit()
    flash(f'Hai terminato il rally con {username}.', 'info')
    
    # Reindirizza l'utente alla pagina da cui proveniva
    return redirect(request.referrer or url_for('main.index'))

# ==============================================================================
# PAGINA PROFILO UTENTE PUBBLICA
# ==============================================================================
@bp.route('/user/<username>')
@login_required
def user_profile(username):
    """Mostra la pagina profilo di un utente specifico."""
    # Troviamo l'utente nel database o restituiamo un errore 404
    user = User.query.filter_by(nome=username).first_or_404()
    
    # Raccogliamo le statistiche per questo utente
    eventi_creati = Event.query.filter_by(creatore=user).count()
    eventi_partecipati = user.eventi_iscritti.count()
    
    return render_template(
        'user_profile.html', 
        user=user, 
        title=f'Profilo di {user.nome}',
        eventi_creati=eventi_creati,
        eventi_partecipati=eventi_partecipati
    )

# ==============================================================================
# PAGINA DI RICERCA GIOCATORI
# ==============================================================================
@bp.route('/players', methods=['GET', 'POST'])
@login_required
def players():
    """Mostra una lista di tutti i giocatori con una barra di ricerca."""
    form = PlayerSearchForm()
    # Inizialmente, la lista 'users' è vuota.
    users = [] 

    # Se il form viene inviato e i dati sono validi...
    if form.validate_on_submit():
        search_term = f"%{form.query.data}%"
        # ...cerchiamo gli utenti il cui nome corrisponde al termine di ricerca,
        # escludendo l'utente attualmente loggato dai risultati.
        users = User.query.filter(User.nome.ilike(search_term), User.id != current_user.id).order_by(User.nome).all()
        if not users:
            flash('Nessun giocatore trovato con quel nome.', 'info')
    
    return render_template('players.html', title='Cerca Giocatori', form=form, users=users)
