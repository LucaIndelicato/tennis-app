from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from app.models import User
from wtforms import BooleanField
from wtforms import RadioField
from wtforms import TextAreaField, SelectField, IntegerField, DateTimeLocalField
from wtforms.validators import NumberRange

class RegistrationForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired(), Length(min=2, max=64)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    cap = StringField('CAP', validators=[DataRequired(), Length(min=5, max=5)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    password2 = PasswordField(
        'Conferma Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Registrati')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Questa email è già stata utilizzata.')
        
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Ricordami')
    submit = SubmitField('Accedi')


class QuizForm(FlaskForm):
    # Dati in formato (valore, etichetta)
    q0_choices = [('0', 'Sto iniziando ora'), ('0.5', 'Da meno di un anno'), ('0.8', 'Da meno di 2 anni'), ('1', 'Oltre i 2 anni')]
    q1_choices = [('0', '< 1h a settimana'), ('0.5', '1h a settimana'), ('0.7', '2h a settimana'), ('0.9', '>2h a settimana')]
    q2_choices = [('0.2', 'Incerto'), ('0.5', 'Costante'), ('1', 'Potente e preciso')]
    q3_choices = [('0.1', 'Spesso a vuoto'), ('0.4', 'Riesco a rispondere'), ('0.7', 'Potente e profondo')]
    # ... puoi continuare a definire le altre domande qui...

    q0 = RadioField("Da quanto tempo giochi a tennis?", choices=q0_choices, validators=[DataRequired()])
    q1 = RadioField("Quanto spesso giochi a tennis?", choices=q1_choices, validators=[DataRequired()])
    q2 = RadioField("Come valuti il tuo dritto?", choices=q2_choices, validators=[DataRequired()])
    q3 = RadioField("Come valuti il tuo rovescio?", choices=q3_choices, validators=[DataRequired()])
    # Aggiungiamo altre 7 domande fittizie per arrivare a 10
    q4 = RadioField("Il tuo servizio è affidabile?", choices=[('1', 'No'), ('2', 'Abbastanza'), ('3', 'Sì')], validators=[DataRequired()])
    q5 = RadioField("Come te la cavi a rete (volée)?", choices=[('1', 'Poco a mio agio'), ('2', 'Mi difendo'), ('3', 'Aggressivo')], validators=[DataRequired()])
    q6 = RadioField("Conosci le regole del tie-break?", choices=[('1', 'No'), ('2', 'In parte'), ('3', 'Sì, perfettamente')], validators=[DataRequired()])
    q7 = RadioField("Riesci a mantenere uno scambio lungo?", choices=[('1', 'Raramente'), ('2', 'A volte'), ('3', 'Sì, con costanza')], validators=[DataRequired()])
    q8 = RadioField("Usi effetti come il top-spin o lo slice?", choices=[('1', 'Mai'), ('2', 'Ogni tanto'), ('3', 'Spesso')], validators=[DataRequired()])
    q9 = RadioField("Come valuti la tua resistenza fisica?", choices=[('1', 'Bassa'), ('2', 'Media'), ('3', 'Alta')], validators=[DataRequired()])
    q10 = RadioField("Qual è il tuo obiettivo principale?", choices=[('1', 'Divertirmi'), ('2', 'Migliorare'), ('3', 'Competere')], validators=[DataRequired()])
    
    submit = SubmitField('Calcola il mio livello')

class EventForm(FlaskForm):
    titolo = StringField('Titolo Evento', validators=[DataRequired(), Length(min=5, max=100)])
    tipologia = SelectField(
        'Tipologia Evento' , 
        choices = [('Partita 1vs1', 'Partita 1vs1'),
            ('Partita 2vs2', 'Partita 2vs2'),
            ('Allenamento guidato', 'Allenamento guidato'),
            ('Lezione', 'Lezione')
        ],
        validators = [DataRequired()]
    )
    descrizione = TextAreaField('Descrizione', validators=[Length(min=0, max=200)])
    data_ora = DateTimeLocalField(
        'Data e Ora',
        format='%Y-%m-%dT%H:%M',
        validators=[DataRequired()]
    )
    luogo = StringField('Luogo (es. Tennis Club Milano)', validators=[DataRequired()])
    max_partecipanti = IntegerField('Numero massimo di partecipanti', validators=[DataRequired(), NumberRange(min=2, max=10)])
    livello_consigliato = SelectField(
        'Livello Consigliato',
        choices=[
            ('Principiante', 'Principiante'),
            ('Intermedio', 'Intermedio'),
            ('Avanzato', 'Avanzato'),
            ('Tutti', 'Tutti i livelli')
        ],
        validators=[DataRequired()]
    )
    submit = SubmitField('Crea Evento')