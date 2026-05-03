from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Session
from reservations.models import Billet


def guide_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('accounts:connexion')
        if not request.user.est_guide():
            messages.error(request, "Accès réservé aux guides.")
            return redirect('catalogue:accueil')
        return view_func(request, *args, **kwargs)
    return wrapper


@login_required(login_url='/accounts/connexion/')
@guide_required
def dashboard(request):
    sessions = Session.objects.filter(
        guide=request.user
    ).order_by('date')

    return render(request, 'guides/dashboard.html', {
        'sessions': sessions
    })


@login_required(login_url='/accounts/connexion/')
@guide_required
def planning(request):
    sessions = Session.objects.filter(guide=request.user)
    return render(request, 'guides/planning.html', {
        'sessions': sessions
    })


@login_required(login_url='/accounts/connexion/')
@guide_required
def pointer(request, code):
    billet = get_object_or_404(Billet, code_qr=code)

    if billet.statut_pointage == 'absent':
        billet.statut_pointage = 'present'
        billet.save()
        messages.success(request, "Présence confirmée !")
    else:
        messages.warning(request, "Ce touriste a déjà été pointé.")

    return redirect('guides:dashboard')