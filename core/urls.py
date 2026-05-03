from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/',          admin.site.urls),
    path('',                include('catalogue.urls')),
    path('accounts/',       include('accounts.urls')),
    path('reservations/',   include('reservations.urls')),
    path('guides/',         include('guides.urls')),
    path('administration/', include('administration.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)