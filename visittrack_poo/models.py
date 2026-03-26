import uuid
import random

class Utilisateur:
    def __init__(self, nom, prenom, email, mot_de_passe, role):
        self.id = None
        self.nom = nom
        self.prenom = prenom
        self.email = email
        self.mot_de_passe = mot_de_passe
        self.role = role  

    def __str__(self):
        return f"{self.prenom} {self.nom} ({self.role})"


class Touriste(Utilisateur):
    def __init__(self, nom, prenom, email, mot_de_passe):
        super().__init__(nom, prenom, email, mot_de_passe, role="touriste")
        self.reservations = [] 

    def reserver(self, circuit, date, nb_participants):
        if circuit.verifier_disponibilite(nb_participants):
            reservation = Reservation(self, circuit, date, nb_participants)
            self.reservations.append(reservation)
            circuit.places_disponibles -= nb_participants
            print(f"Réservation confirmée : {circuit.titre} le {date}")
            return reservation
        else:
            print("Désolé, plus de places disponibles.")
            return None

    def annuler(self, reservation):
        if reservation in self.reservations:
            reservation.statut = "annulée"
            reservation.circuit.places_disponibles += reservation.nb_participants
            self.reservations.remove(reservation)
            print(f"Réservation annulée : {reservation.circuit.titre}")


class Guide(Utilisateur):
    def __init__(self, nom, prenom, email, mot_de_passe, specialites):
        super().__init__(nom, prenom, email, mot_de_passe, role="guide")
        self.specialites = specialites
        self.planning = []

    def pointer_presence(self, billet):
        if billet.statut_pointage == "absent":
            billet.statut_pointage = "present"
            print(f"Présence confirmée : {billet.reservation.touriste}")
        else:
            print("Déjà pointé.")

    def __str__(self):
        return f"Guide : {self.prenom} {self.nom} | Spécialités : {self.specialites}"


class Admin(Utilisateur):
    def __init__(self, nom, prenom, email, mot_de_passe):
        super().__init__(nom, prenom, email, mot_de_passe, role="admin")

    def affecter_guide(self, guide, session):
        if session not in guide.planning:
            guide.planning.append(session)
            session.guide = guide
            print(f"Guide {guide.prenom} affecté à : {session.circuit.titre}")
        else:
            print("Conflit de planning détecté !")


class Circuit:
    def __init__(self, titre, destination, duree, prix, capacite_max):
        self.id = None
        self.titre = titre
        self.destination = destination
        self.duree = duree               
        self.prix = prix                
        self.capacite_max = capacite_max
        self.places_disponibles = capacite_max
        self.statut = "actif"

    def verifier_disponibilite(self, nb_participants):
        return self.places_disponibles >= nb_participants

    def __str__(self):
        return f"{self.titre} → {self.destination} | {self.prix} MAD | Places : {self.places_disponibles}/{self.capacite_max}"


class Session:
    def __init__(self, circuit, date, heure, lieu_rdv):
        self.id = None
        self.circuit = circuit
        self.date = date
        self.heure = heure
        self.lieu_rdv = lieu_rdv
        self.guide = None
        self.participants = []

    def __str__(self):
        return f"Session : {self.circuit.titre} | {self.date} à {self.heure} | RDV : {self.lieu_rdv}"


class Billet:
    def __init__(self, reservation):
        self.id = None
        self.reservation = reservation
        self.code_qr = str(uuid.uuid4())
        self.statut_pointage = "absent"

    def __str__(self):
        return f"Billet [{self.code_qr[:8]}...] | Pointage : {self.statut_pointage}"


class Reservation:
    _compteur = 0

    def __init__(self, touriste, circuit, date, nb_participants):
        Reservation._compteur += 1
        self.id = Reservation._compteur 
        self.touriste = touriste
        self.circuit = circuit
        self.date = date
        self.nb_participants = nb_participants
        self.statut = "confirmée"
        self.montant_total = circuit.prix * nb_participants
        self.billet = Billet(self)

    def __str__(self):
        return (f"Réservation #{self.id} | {self.circuit.titre} | "
                f"{self.nb_participants} pers. | {self.montant_total} MAD | {self.statut}")


class Paiement:
    def __init__(self, reservation, methode="carte"):
        self.id = None
        self.reservation = reservation
        self.montant = reservation.montant_total
        self.methode = methode
        self.statut = "en_attente"
        self.reference = str(uuid.uuid4())[:12].upper()

    def confirmer(self):
        self.statut = "confirmé"
        print(f"Paiement confirmé : {self.montant} MAD | Réf : {self.reference}")

    def __str__(self):
        return f"Paiement {self.reference} | {self.montant} MAD | {self.statut}"


        