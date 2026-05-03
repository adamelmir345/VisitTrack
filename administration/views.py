from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from catalogue.models import Circuit
from reservations.models import Reservation
from accounts.models import Utilisateur


def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('accounts:connexion')
        if not request.user.est_admin():
            messages.error(request, "Accès réservé aux administrateurs.")
            return redirect('catalogue:accueil')
        return view_func(request, *args, **kwargs)
    return wrapper


@login_required(login_url='/accounts/connexion/')
@admin_required
def dashboard(request):
    return render(request, 'administration/dashboard.html', {
        'nb_circuits'     : Circuit.objects.count(),
        'nb_reservations' : Reservation.objects.count(),
        'nb_guides'       : Utilisateur.objects.filter(role='guide').count(),
        'nb_touristes'    : Utilisateur.objects.filter(role='touriste').count(),
        'reservations'    : Reservation.objects.order_by('-date_creation')[:5],
    })


@login_required(login_url='/accounts/connexion/')
@admin_required
def gerer_circuits(request):
    circuits = Circuit.objects.all().order_by('-date_creation')
    return render(request, 'administration/circuits.html', {
        'circuits': circuits
    })


@login_required(login_url='/accounts/connexion/')
@admin_required
def ajouter_circuit(request):
    if request.method == 'POST':
        Circuit.objects.create(
            titre              = request.POST['titre'],
            description        = request.POST['description'],
            destination        = request.POST['destination'],
            duree              = int(request.POST['duree']),
            prix               = float(request.POST['prix']),
            capacite_max       = int(request.POST['capacite_max']),
            places_disponibles = int(request.POST['capacite_max']),
            statut             = 'actif'
        )
        messages.success(request, "Circuit ajouté avec succès !")
        return redirect('administration:circuits')

    return render(request, 'administration/ajouter_circuit.html')


@login_required(login_url='/accounts/connexion/')
@admin_required
def gerer_reservations(request):
    reservations = Reservation.objects.all().order_by('-date_creation')
    return render(request, 'administration/reservations.html', {
        'reservations': reservations
    })


@login_required(login_url='/accounts/connexion/')
@admin_required
def gerer_guides(request):
    guides = Utilisateur.objects.filter(role='guide')
    return render(request, 'administration/guides.html', {
        'guides': guides
    })