from django.shortcuts import render


def obedi_portfolio(request):
    return render(request, "portfolios/obedi.html")
