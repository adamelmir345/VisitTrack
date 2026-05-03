from django.shortcuts import render, get_object_or_404
from .models import Circuit


def accueil(request):
    circuits = Circuit.objects.filter(statut='actif')[:6]
    return render(request, 'catalogue/accueil.html', {
        'circuits': circuits
    })


def liste_circuits(request):
    circuits = Circuit.objects.filter(statut='actif')
    return render(request, 'catalogue/liste.html', {
        'circuits': circuits
    })


def detail_circuit(request, pk):
    circuit = get_object_or_404(Circuit, pk=pk)
    return render(request, 'catalogue/detail.html', {
        'circuit': circuit
    })