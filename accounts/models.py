from django.contrib.auth.models import AbstractUser
from django.db import models


class Utilisateur(AbstractUser):
    ROLES = [
        ('touriste',       'Touriste'),
        ('guide',          'Guide'),
        ('administrateur', 'Administrateur'),
    ]
    role = models.CharField(
        max_length=20,
        choices=ROLES,
        default='touriste'
    )
    telephone = models.CharField(max_length=20, blank=True)
    photo     = models.ImageField(
        upload_to='photos/',
        blank=True,
        null=True
    )

    def est_touriste(self):
        return self.role == 'touriste'

    def est_guide(self):
        return self.role == 'guide'

    def est_admin(self):
        return self.role == 'administrateur'

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.role})"