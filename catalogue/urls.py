from django.urls import path
from . import views

app_name = 'catalogue'

urlpatterns = [
    path('',                views.accueil,         name='accueil'),
    path('circuits/',       views.liste_circuits,  name='liste'),
    path('circuits/<int:pk>/', views.detail_circuit, name='detail'),
]