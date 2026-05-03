from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Utilisateur


# ──────────────────────────────────────────
# INSCRIPTION
# ──────────────────────────────────────────
def inscription(request):
    if request.user.is_authenticated:
        return redirect('catalogue:accueil')

    if request.method == 'POST':
        nom      = request.POST.get('nom', '').strip()
        prenom   = request.POST.get('prenom', '').strip()
        email    = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')

        # Vérifications
        if not all([nom, prenom, email, password]):
            messages.error(request, "Tous les champs sont obligatoires.")
            return redirect('accounts:inscription')

        if Utilisateur.objects.filter(email=email).exists():
            messages.error(request, "Cet email est déjà utilisé.")
            return redirect('accounts:inscription')

        if len(password) < 6:
            messages.error(request, "Le mot de passe doit faire au moins 6 caractères.")
            return redirect('accounts:inscription')

        # Création du compte
        user = Utilisateur.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=prenom,
            last_name=nom,
            role='touriste'
        )
        login(request, user)
        messages.success(request, f"Bienvenue {prenom} ! Votre compte a été créé.")
        return redirect('catalogue:accueil')

    return render(request, 'accounts/inscription.html')


# ──────────────────────────────────────────
# CONNEXION
# ──────────────────────────────────────────
def connexion(request):
    if request.user.is_authenticated:
        return redirect('catalogue:accueil')

    if request.method == 'POST':
        email    = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        user     = authenticate(request, username=email, password=password)

        if user:
            login(request, user)
            messages.success(request, f"Bienvenue {user.first_name} !")

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


# ──────────────────────────────────────────
# DÉCONNEXION
# ──────────────────────────────────────────
def deconnexion(request):
    logout(request)
    messages.success(request, "Vous avez été déconnecté.")
    return redirect('catalogue:accueil')


# ──────────────────────────────────────────
# PROFIL
# ──────────────────────────────────────────
@login_required(login_url='/accounts/connexion/')
def profil(request):
    return render(request, 'accounts/profil.html', {
        'user': request.user
    })