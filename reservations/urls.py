from django.urls import path
from . import views

app_name = 'reservations'

urlpatterns = [
    path('reserver/<int:circuit_id>/', views.reserver,          name='reserver'),
    path('mes-reservations/',          views.mes_reservations,  name='mes_reservations'),
    path('billet/<int:reservation_id>/', views.telecharger_billet, name='billet'),
]