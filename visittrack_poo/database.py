import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "visittrack.db")


# ──────────────────────────────────────────
# CONNEXION
# ──────────────────────────────────────────
def get_connexion():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


# ──────────────────────────────────────────
# CRÉATION DES TABLES
# ──────────────────────────────────────────
def creer_tables():
    conn = get_connexion()
    cursor = conn.cursor()
    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS utilisateurs (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            nom          TEXT NOT NULL,
            prenom       TEXT NOT NULL,
            email        TEXT UNIQUE NOT NULL,
            mot_de_passe TEXT NOT NULL,
            role         TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS circuits (
            id                 INTEGER PRIMARY KEY AUTOINCREMENT,
            titre              TEXT NOT NULL,
            destination        TEXT NOT NULL,
            duree              INTEGER NOT NULL,
            prix               REAL NOT NULL,
            capacite_max       INTEGER NOT NULL,
            places_disponibles INTEGER NOT NULL,
            statut             TEXT DEFAULT 'actif'
        );

        CREATE TABLE IF NOT EXISTS reservations (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            touriste_id     INTEGER NOT NULL,
            circuit_id      INTEGER NOT NULL,
            date            TEXT NOT NULL,
            nb_participants INTEGER NOT NULL,
            statut          TEXT DEFAULT 'confirmee',
            montant_total   REAL NOT NULL,
            FOREIGN KEY (touriste_id) REFERENCES utilisateurs(id),
            FOREIGN KEY (circuit_id)  REFERENCES circuits(id)
        );

        CREATE TABLE IF NOT EXISTS billets (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            reservation_id  INTEGER NOT NULL,
            code_qr         TEXT UNIQUE NOT NULL,
            statut_pointage TEXT DEFAULT 'absent',
            FOREIGN KEY (reservation_id) REFERENCES reservations(id)
        );

        CREATE TABLE IF NOT EXISTS paiements (
            id             INTEGER PRIMARY KEY AUTOINCREMENT,
            reservation_id INTEGER NOT NULL,
            montant        REAL NOT NULL,
            methode        TEXT DEFAULT 'carte',
            statut         TEXT DEFAULT 'en_attente',
            reference      TEXT UNIQUE NOT NULL,
            FOREIGN KEY (reservation_id) REFERENCES reservations(id)
        );
    """)
    conn.commit()
    conn.close()
    print("Tables creees avec succes.")


# ──────────────────────────────────────────
# CRUD — UTILISATEURS
# ──────────────────────────────────────────
def sauvegarder_utilisateur(utilisateur):
    conn = get_connexion()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO utilisateurs (nom, prenom, email, mot_de_passe, role)
        VALUES (?, ?, ?, ?, ?)
    """, (utilisateur.nom, utilisateur.prenom,
          utilisateur.email, utilisateur.mot_de_passe,
          utilisateur.role))
    conn.commit()
    utilisateur.id = cursor.lastrowid
    conn.close()
    print(f"Utilisateur sauvegarde : {utilisateur}")


def charger_utilisateurs():
    conn = get_connexion()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM utilisateurs")
    rows = cursor.fetchall()
    conn.close()
    return rows


# ──────────────────────────────────────────
# CRUD — CIRCUITS
# ──────────────────────────────────────────
def sauvegarder_circuit(circuit):
    conn = get_connexion()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO circuits
            (titre, destination, duree, prix,
             capacite_max, places_disponibles, statut)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (circuit.titre, circuit.destination,
          circuit.duree, circuit.prix,
          circuit.capacite_max, circuit.places_disponibles,
          circuit.statut))
    conn.commit()
    circuit.id = cursor.lastrowid
    conn.close()
    print(f"Circuit sauvegarde : {circuit}")


def charger_circuits():
    conn = get_connexion()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM circuits WHERE statut = 'actif'")
    rows = cursor.fetchall()
    conn.close()
    return rows


def modifier_circuit(circuit_id, nouvelles_valeurs: dict):
    conn = get_connexion()
    cursor = conn.cursor()
    for colonne, valeur in nouvelles_valeurs.items():
        cursor.execute(
            f"UPDATE circuits SET {colonne} = ? WHERE id = ?",
            (valeur, circuit_id)
        )
    conn.commit()
    conn.close()
    print(f"Circuit {circuit_id} modifie.")


def supprimer_circuit(circuit_id):
    conn = get_connexion()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM circuits WHERE id = ?", (circuit_id,))
    conn.commit()
    conn.close()
    print(f"Circuit {circuit_id} supprime.")


# ──────────────────────────────────────────
# CRUD — RESERVATIONS
# ──────────────────────────────────────────
def sauvegarder_reservation(reservation):
    conn = get_connexion()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO reservations
            (touriste_id, circuit_id, date,
             nb_participants, statut, montant_total)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (reservation.touriste.id, reservation.circuit.id,
          reservation.date, reservation.nb_participants,
          reservation.statut, reservation.montant_total))
    conn.commit()
    reservation.id = cursor.lastrowid
    conn.close()
    print(f"Reservation sauvegardee : {reservation}")


def charger_reservations():
    conn = get_connexion()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM reservations")
    rows = cursor.fetchall()
    conn.close()
    return rows


# ──────────────────────────────────────────
# CRUD — BILLETS
# ──────────────────────────────────────────
def sauvegarder_billet(billet, reservation_id):
    conn = get_connexion()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO billets (reservation_id, code_qr, statut_pointage)
        VALUES (?, ?, ?)
    """, (reservation_id, billet.code_qr, billet.statut_pointage))
    conn.commit()
    conn.close()
    print(f"Billet sauvegarde : {billet}")


def pointer_billet(code_qr):
    conn = get_connexion()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE billets
        SET statut_pointage = 'present'
        WHERE code_qr = ? AND statut_pointage = 'absent'
    """, (code_qr,))
    conn.commit()
    modifie = cursor.rowcount
    conn.close()
    if modifie:
        print(f"Presence confirmee : {code_qr[:8]}...")
    else:
        print("Billet deja pointe ou introuvable.")


# ──────────────────────────────────────────
# CRUD — PAIEMENTS
# ──────────────────────────────────────────
def sauvegarder_paiement(paiement, reservation_id):
    conn = get_connexion()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO paiements
            (reservation_id, montant, methode, statut, reference)
        VALUES (?, ?, ?, ?, ?)
    """, (reservation_id, paiement.montant,
          paiement.methode, paiement.statut,
          paiement.reference))
    conn.commit()
    conn.close()
    print(f"Paiement sauvegarde : {paiement}")