from django.shortcuts import render

def dashboard(request):
    return render(request, 'administration/dashboard.html')

def gerer_circuits(request):
    return render(request, 'administration/circuits.html')

def ajouter_circuit(request):
    return render(request, 'administration/ajouter_circuit.html')

def gerer_reservations(request):
    return render(request, 'administration/reservations.html')

def gerer_guides(request):
    return render(request, 'administration/guides.html')
