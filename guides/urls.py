from django.urls import path
from . import views

app_name = 'guides'

urlpatterns = [
    path('dashboard/',          views.dashboard,     name='dashboard'),
    path('planning/',           views.planning,      name='planning'),
    path('pointer/<str:code>/', views.pointer,       name='pointer'),
]