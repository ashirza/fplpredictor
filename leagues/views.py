from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views import generic

from leagues.models import League


class IndexView(generic.ListView):
    template_name = 'leagues/index.html'
    context_object_name = "leagues"

    def get_queryset(self):
        return League.objects.all()


class DetailView(generic.DetailView):
    model = League
    template_name = 'leagues/detail.html'
