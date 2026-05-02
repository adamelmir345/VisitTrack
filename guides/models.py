from django.db import models
from accounts.models import Utilisateur
from catalogue.models import Circuit


class Session(models.Model):
    circuit  = models.ForeignKey(
        Circuit,
        on_delete=models.CASCADE,
        related_name='sessions'
    )
    guide    = models.ForeignKey(
        Utilisateur,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='sessions'
    )
    date     = models.DateField()
    heure    = models.TimeField()
    lieu_rdv = models.CharField(max_length=300)

    def __str__(self):
        return f"{self.circuit.titre} – {self.date} – {self.guide}"

    class Meta:
        ordering = ['date', 'heure']