from django.contrib import admin
from .models import League
# Register your models here.


class LeagueAdmin(admin.ModelAdmin):
    fields = ["name"]
    list_display = ["name"]

admin.site.register(League)
