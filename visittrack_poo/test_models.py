from models import Touriste, Guide, Admin, Circuit, Session, Paiement
from database import (
    creer_tables,
    sauvegarder_utilisateur, charger_utilisateurs,
    sauvegarder_circuit, charger_circuits,
    sauvegarder_reservation, charger_reservations,
    sauvegarder_billet, pointer_billet,
    sauvegarder_paiement
)
from generateurs import GenerateurQR, GenerateurPDF
from database import modifier_circuit


# ── Créer les objets ──────────────────────
circuit = Circuit("Trekking Toubkal", "Marrakech", 3, 800, 20)
touriste = Touriste("Ali", "Nabil", "nabil@email.com", "1234")
guide = Guide("Zmirili", "Yassine", "yassine@email.com", "1234", ["montagne", "désert"])
admin = Admin("Elmir", "Adam", "adam@email.com", "1234")


print(circuit)
print(touriste)
print(guide)

reservation = touriste.reserver(circuit, "2026-04-10", 2)
print(reservation)
print(reservation.billet)

paiement = Paiement(reservation)
paiement.confirmer()


session = Session(circuit, "2026-04-10", "08:00", "Place Jemaa el-Fna")
admin.affecter_guide(guide, session)

guide.pointer_presence(reservation.billet)
print(reservation.billet)




gen_qr = GenerateurQR()
chemin_qr = gen_qr.generer(
    code=reservation.billet.code_qr,
    nom_fichier=f"billet_{reservation.id}.png"
)

# Générer le PDF
gen_pdf = GenerateurPDF()
chemin_pdf = gen_pdf.creer_billet(reservation, chemin_qr)

print(f"\nFichiers generes :")
print(f"  QR Code : {chemin_qr}")
print(f"  PDF     : {chemin_pdf}")

print("\n── TEST BASE DE DONNEES ──")

# Créer les tables
creer_tables()

# Sauvegarder
sauvegarder_utilisateur(touriste)
sauvegarder_circuit(circuit)
sauvegarder_reservation(reservation)
sauvegarder_billet(reservation.billet, reservation.id)
sauvegarder_paiement(paiement, reservation.id)

print("\nUtilisateurs en base :")
for u in charger_utilisateurs():
    print(dict(u))

print("\nCircuits en base :")
for c in charger_circuits():
    print(dict(c))

print("\nReservations en base :")
for r in charger_reservations():
    print(dict(r))


pointer_billet(reservation.billet.code_qr)



modifier_circuit(circuit.id, {"prix": 900, "statut": "actif"})

print("\nCircuit apres modification :")
for c in charger_circuits():
    print(dict(c))

    