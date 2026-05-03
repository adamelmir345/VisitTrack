from django.shortcuts import render

def dashboard(request):
    return render(request, 'guides/dashboard.html')

def planning(request):
    return render(request, 'guides/planning.html')

def pointer(request, code):
    # Logique pour scanner un billet
    return render(request, 'guides/pointer.html')
