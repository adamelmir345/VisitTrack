from django.urls import path
from . import views

app_name = 'administration'

urlpatterns = [
    path('',                      views.dashboard,         name='dashboard'),
    path('circuits/',             views.gerer_circuits,    name='circuits'),
    path('circuits/ajouter/',     views.ajouter_circuit,   name='ajouter_circuit'),
    path('reservations/',         views.gerer_reservations,name='reservations'),
    path('guides/',               views.gerer_guides,      name='guides'),
]