from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import generic
from django.urls import reverse

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


class LeagueJoinForm(forms.Form):
    join_code = forms.UUIDField(label="Join Code", required=True)


def join(request):
    if request.method == "POST":
        form = LeagueJoinForm(request.POST)
        if form.is_valid():
            request.user.leagues.add(
                League.objects.get(join_code=form.cleaned_data["join_code"])
            )
            return HttpResponseRedirect(reverse("index"))
