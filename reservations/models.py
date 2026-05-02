from django.db import models
from accounts.models import Utilisateur
from catalogue.models import Circuit
import uuid


class Reservation(models.Model):
    STATUTS = [
        ('confirmee', 'Confirmée'),
        ('annulee',   'Annulée'),
        ('en_attente','En attente'),
    ]
    touriste        = models.ForeignKey(
        Utilisateur,
        on_delete=models.CASCADE,
        related_name='reservations'
    )
    circuit         = models.ForeignKey(
        Circuit,
        on_delete=models.CASCADE,
        related_name='reservations'
    )
    date            = models.DateField()
    nb_participants = models.IntegerField()
    statut          = models.CharField(
        max_length=20,
        choices=STATUTS,
        default='confirmee'
    )
    montant_total   = models.FloatField()
    date_creation   = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Calcul automatique du montant
        self.montant_total = self.circuit.prix * self.nb_participants
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Reservation #{self.id} – {self.circuit.titre}"

    class Meta:
        ordering = ['-date_creation']


class Billet(models.Model):
    reservation     = models.OneToOneField(
        Reservation,
        on_delete=models.CASCADE,
        related_name='billet'
    )
    code_qr         = models.UUIDField(default=uuid.uuid4, unique=True)
    statut_pointage = models.CharField(
        max_length=10,
        default='absent'
    )
    date_emission   = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Billet {str(self.code_qr)[:8]} – {self.statut_pointage}"


class Paiement(models.Model):
    STATUTS = [
        ('en_attente', 'En attente'),
        ('confirme',   'Confirmé'),
        ('rembourse',  'Remboursé'),
    ]
    reservation = models.OneToOneField(
        Reservation,
        on_delete=models.CASCADE,
        related_name='paiement'
    )
    montant     = models.FloatField()
    methode     = models.CharField(max_length=50, default='carte')
    statut      = models.CharField(
        max_length=20,
        choices=STATUTS,
        default='en_attente'
    )
    reference   = models.UUIDField(default=uuid.uuid4, unique=True)
    date        = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Paiement {str(self.reference)[:8]} – {self.statut}"