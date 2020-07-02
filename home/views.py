from django.shortcuts import render


def index(request):
    """Return the index.html file"""
    return render(request, 'index.html')


def http404(request):
    return render(request, "404.html")


def http500(request):
    return render(request, "500.html")
