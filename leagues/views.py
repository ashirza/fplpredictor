from django.shortcuts import render
from django.views import generic

from leagues.models import League


def index(request):
    leagues = request.user.leagues.all()
    context = {
        "leagues": leagues,
    }
    return render(request, "leagues/index.html", context)


class DetailView(generic.DetailView):
    model = League
    template_name = "leagues/detail.html"
