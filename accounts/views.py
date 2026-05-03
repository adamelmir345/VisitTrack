from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .models import Utilisateur


def inscription(request):
    if request.method == 'POST':
        nom      = request.POST['nom']
        prenom   = request.POST['prenom']
        email    = request.POST['email']
        password = request.POST['password']

        if Utilisateur.objects.filter(email=email).exists():
            messages.error(request, "Cet email est déjà utilisé.")
            return redirect('accounts:inscription')

        user = Utilisateur.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=prenom,
            last_name=nom,
            role='touriste'
        )
        login(request, user)
        messages.success(request, "Compte créé avec succès !")
        return redirect('catalogue:accueil')

    return render(request, 'accounts/inscription.html')


def connexion(request):
    if request.method == 'POST':
        email    = request.POST['email']
        password = request.POST['password']
        user     = authenticate(request, username=email, password=password)

        if user:
            login(request, user)
            # Redirection selon le rôle
            if user.est_admin():
                return redirect('administration:dashboard')
            elif user.est_guide():
                return redirect('guides:dashboard')
            else:
                return redirect('catalogue:accueil')
        else:
            messages.error(request, "Email ou mot de passe incorrect.")

    return render(request, 'accounts/connexion.html')


def deconnexion(request):
    logout(request)
    return redirect('catalogue:accueil')


def profil(request):
    return render(request, 'accounts/profil.html')