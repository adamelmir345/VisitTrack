from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from catalogue.models import Circuit
from .models import Reservation, Billet


def touriste_required(view_func):
    """Décorateur personnalisé — réservé aux touristes"""
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('accounts:connexion')
        if not request.user.est_touriste():
            messages.error(request, "Accès réservé aux touristes.")
            return redirect('catalogue:accueil')
        return view_func(request, *args, **kwargs)
    return wrapper


@login_required(login_url='/accounts/connexion/')
@touriste_required
def reserver(request, circuit_id):
    circuit = get_object_or_404(Circuit, pk=circuit_id, statut='actif')

    if request.method == 'POST':
        nb  = int(request.POST.get('nb_participants', 1))
        date = request.POST.get('date')

        if not circuit.verifier_disponibilite(nb):
            messages.error(request, "Pas assez de places disponibles.")
            return redirect('catalogue:detail', pk=circuit_id)

        reservation = Reservation.objects.create(
            touriste=request.user,
            circuit=circuit,
            date=date,
            nb_participants=nb,
            montant_total=circuit.prix * nb,
            statut='confirmee'
        )

        # Créer le billet automatiquement
        Billet.objects.create(reservation=reservation)

        # Mettre à jour les places
        circuit.places_disponibles -= nb
        circuit.save()

        messages.success(request, "Réservation confirmée ! Votre billet a été généré.")
        return redirect('reservations:mes_reservations')

    return render(request, 'reservations/reserver.html', {
        'circuit': circuit
    })


@login_required(login_url='/accounts/connexion/')
def mes_reservations(request):
    reservations = Reservation.objects.filter(
        touriste=request.user
    ).order_by('-date_creation')

    return render(request, 'reservations/mes_reservations.html', {
        'reservations': reservations
    })


@login_required(login_url='/accounts/connexion/')
def telecharger_billet(request, reservation_id):
    reservation = get_object_or_404(
        Reservation,
        pk=reservation_id,
        touriste=request.user
    )
    return render(request, 'reservations/billet.html', {
        'reservation': reservation,
        'billet': reservation.billet
    })