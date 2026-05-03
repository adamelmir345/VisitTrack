from django.shortcuts import render

def reserver(request, circuit_id):
    return render(request, 'reservations/reserver.html')

def mes_reservations(request):
    return render(request, 'reservations/mes_reservations.html')

def telecharger_billet(request, reservation_id):
    # Logique à venir
    pass
