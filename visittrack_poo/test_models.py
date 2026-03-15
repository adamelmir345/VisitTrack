from models import Touriste, Guide, Admin, Circuit, Session, Paiement

# ── Créer les objets ──────────────────────
circuit = Circuit("Trekking Toubkal", "Marrakech", 3, 800, 20)
touriste = Touriste("Ali", "Nabil", "nabil@email.com", "1234")
guide = Guide("Zmirili", "Yassine", "yassine@email.com", "1234", ["montagne", "désert"])
admin = Admin("Elmir", "Adam", "adam@email.com", "1234")

# ── Afficher ─────────────────────────────
print(circuit)
print(touriste)
print(guide)

# ── Réserver ─────────────────────────────
reservation = touriste.reserver(circuit, "2026-04-10", 2)
print(reservation)
print(reservation.billet)

# ── Paiement ─────────────────────────────
paiement = Paiement(reservation)
paiement.confirmer()

# ── Affecter guide ────────────────────────
session = Session(circuit, "2026-04-10", "08:00", "Place Jemaa el-Fna")
admin.affecter_guide(guide, session)

# ── Pointer présence ──────────────────────
guide.pointer_presence(reservation.billet)
print(reservation.billet)