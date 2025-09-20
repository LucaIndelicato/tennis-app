<div align="center">
  <!-- <img src="https://raw.githubusercontent.com/LucaIndelicato/tennis-app/main/app/static/logo.png" alt="TennisApp Logo" width="150"/> -->
  <h1><b>TennisApp 🎾</b></h1>
  <p>Una web app social per giocatori di tennis amatoriali. Organizza partite, trova nuovi avversari e cresci nella community!</p>
  
  <p>
    <img src="https://img.shields.io/badge/Python-3.11+-blue.svg?style=for-the-badge&logo=python&logoColor=white" alt="Python Version">
    <img src="https://img.shields.io/badge/Flask-3.0+-black.svg?style=for-the-badge&logo=flask&logoColor=white" alt="Flask Version">
    <img src="https://img.shields.io/github/license/LucaIndelicato/tennis-app?style=for-the-badge" alt="License">
  </p>
</div>

---

## 🎯 Informazioni sul Progetto

**TennisApp** nasce con l'obiettivo di risolvere un problema comune per molti tennisti amatoriali: la difficoltà di trovare partner di gioco e organizzare partite. Questa applicazione web, costruita con il framework Flask, fornisce una piattaforma centralizzata dove gli utenti possono creare e partecipare a eventi tennistici, connettersi con altri giocatori e tenere traccia delle proprie attività.

Il progetto è sviluppato come un **Minimum Viable Product (MVP)**, con una solida base per future espansioni e l'introduzione di funzionalità ancora più social e interattive.

<br>

## ✨ Funzionalità Principali

L'applicazione offre un set di funzionalità completo per gestire l'esperienza di un tennista:

* 👤 **Autenticazione Utente:** Sistema completo di registrazione, login e gestione della sessione.
* 📝 **Gestione Profilo:** Ogni utente ha una bacheca personale e un profilo pubblico. Può modificare i propri dati anagrafici e tenere traccia delle sue statistiche.
* 🏆 **Quiz di Livello:** Un quiz interattivo per aiutare i giocatori a definire il proprio livello di gioco (Principiante, Intermedio, Avanzato).
* 🗓️ **Creazione e Gestione Eventi:** Gli utenti possono creare nuovi eventi (partite, allenamenti) specificando dettagli come luogo, data, ora e livello consigliato. Il creatore può anche modificare o cancellare i propri eventi.
* 🔍 **Ricerca e Filtro Eventi:** Una pagina dedicata permette di cercare e filtrare tutti gli eventi disponibili per titolo, luogo, data o tipologia, con un'interfaccia pulita e intuitiva.
* 🤝 **Sistema di "Rally" (Follow):** Gli utenti possono connettersi tra loro seguendosi a vicenda. Questo permette di rimanere aggiornati sulle attività dei propri giocatori preferiti.
* 🔎 **Ricerca Giocatori:** Una sezione dedicata per cercare altri utenti per nome e visitare i loro profili pubblici.

<br>

## 🛠️ Stack Tecnologico

Questo progetto è costruito utilizzando tecnologie moderne e consolidate nel mondo Python:

* **Backend:** **Python** con il micro-framework **Flask**.
* **Database:** **SQLAlchemy** come ORM per interagire con un database **SQLite** in sviluppo.
* **Gestione Form:** **Flask-WTF** per una gestione sicura e validata dei form.
* **Autenticazione:** **Flask-Login** per gestire le sessioni utente.
* **Frontend:** **HTML** con template engine **Jinja2**.
* **Styling:** **Tailwind CSS** per un'interfaccia moderna e responsive.
* **Interattività:** **jQuery** e **Select2** per migliorare l'usabilità dei filtri di ricerca.

<br>

## 🚀 Come Iniziare

Per avviare il progetto in locale sul tuo computer, segui questi semplici passaggi.

1.  **Clona il Repository**
    ```bash
    git clone [https://github.com/LucaIndelicato/tennis-app.git](https://github.com/LucaIndelicato/tennis-app.git)
    cd tennis-app
    ```

2.  **Crea e Attiva un Ambiente Virtuale**
    ```bash
    # Per Windows
    python -m venv venv
    .\venv\Scripts\activate

    # Per macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Installa le Dipendenze**
    Il progetto utilizza le librerie elencate nel file `requirements.txt`.
    ```bash
    pip install -r requirements.txt
    ```

4.  **Inizializza il Database**
    Per creare un database pulito con tutte le tabelle necessarie, esegui lo script fornito.
    ```bash
    python reset_database.py
    ```

5.  **Avvia l'Applicazione**
    Lancia il server di sviluppo Flask.
    ```bash
    python run.py
    ```
    L'applicazione sarà ora accessibile all'indirizzo `http://127.0.0.1:5000`.

<br>
## 📂 Struttura del Progetto
Il codice è organizzato seguendo le best practice del pattern **Application Factory** per garantire modularità e scalabilità.

```
tennis-app/
├── app/                  # Cuore dell'applicazione Flask
│   ├── static/           # File statici (CSS, JS, immagini)
│   ├── templates/        # Template HTML con Jinja2
│   ├── init.py       # Application Factory (create_app)
│   ├── forms.py          # Definizione dei form con Flask-WTF
│   ├── models.py         # Modelli del database con SQLAlchemy
│   └── routes.py         # Logica delle view e routing con Blueprints
│
├── instance/             # Cartella per file non versionati (es. app.db)
│   └── app.db            # Database SQLite
│
├── venv/                 # Ambiente virtuale Python (non tracciato da Git)
│
├── config.py             # File di configurazione (chiavi segrete, URI DB)
├── requirements.txt      # Elenco delle dipendenze Python
├── run.py                # Script per avviare l'applicazione
└── README.md             # Questo file!
```