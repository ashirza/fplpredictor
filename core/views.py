from django.shortcuts import render


# Create your views here.
def index(request):
    leagues = request.user.leagues.all()
    context = {
        "leagues": leagues,
    }
    return render(request, "core/index.html", context)
