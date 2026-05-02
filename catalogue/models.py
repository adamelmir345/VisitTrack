from django.db import models


class Circuit(models.Model):
    STATUTS = [
        ('actif',   'Actif'),
        ('inactif', 'Inactif'),
    ]
    titre              = models.CharField(max_length=200)
    description        = models.TextField()
    destination        = models.CharField(max_length=200)
    duree              = models.IntegerField(help_text="Durée en jours")
    prix               = models.FloatField()
    capacite_max       = models.IntegerField()
    places_disponibles = models.IntegerField()
    statut             = models.CharField(
        max_length=10,
        choices=STATUTS,
        default='actif'
    )
    date_creation = models.DateTimeField(auto_now_add=True)
    image         = models.ImageField(
        upload_to='circuits/',
        blank=True,
        null=True
    )

    def verifier_disponibilite(self, nb):
        return self.places_disponibles >= nb

    def __str__(self):
        return f"{self.titre} – {self.destination}"

    class Meta:
        ordering = ['-date_creation']
        verbose_name = "Circuit"
        verbose_name_plural = "Circuits"