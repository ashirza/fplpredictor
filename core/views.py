from django.shortcuts import render
from django.http import JsonResponse
from .fpl_client import FplClient
from .models import Fixture, Prediction
from .forms import PredictionForm


# Create your views here.
def index(request):
    leagues = request.user.leagues.all()

    fpl_client = FplClient()
    current_gameweek = fpl_client.get_current_gameweek()
    fixtures = Fixture.objects.filter(
        gameweek__in=[current_gameweek, current_gameweek + 1]
    )

    user_predictions = Prediction.objects.filter(
        user=request.user, fixture__in=fixtures
    ).select_related("fixture")

    predictions_dict = {p.fixture_id: p for p in user_predictions}

    completed_fixtures = []
    upcoming_fixtures = []

    for fixture in fixtures:
        fixture_data = {
            "fixture": fixture,
            "prediction": predictions_dict.get(fixture.id),
            "can_predict": fixture.status in ["SCHEDULED", "TIMED"],
        }
        if fixture.status == "FINISHED":
            completed_fixtures.append(fixture_data)
        else:
            upcoming_fixtures.append(fixture_data)

    context = {
        "leagues": leagues,
        "completed_fixtures": completed_fixtures,
        "upcoming_fixtures": upcoming_fixtures,
    }
    return render(request, "core/index.html", context)


def fixtures(request):
    fpl_client = FplClient()
    current_gameweek = fpl_client.get_current_gameweek()
    current_fixtures = Fixture.objects.filter(gameweek=current_gameweek)

    user_predictions = Prediction.objects.filter(
        user=request.user, fixture__in=current_fixtures
    ).select_related("fixture")

    predictions_dict = {p.fixture_id: p for p in user_predictions}

    context = {
        "fixtures": [
            {
                "fixture": fixture,
                "prediction": predictions_dict.get(fixture.id),
                "can_predict": fixture.status == "SCHEDULED",
            }
            for fixture in current_fixtures
        ]
    }
    return render(request, "core/fixtures.html", context)


def predict(request, fixture_id):
    fixture = Fixture.objects.get(id=fixture_id)
    if fixture.status not in ["SCHEDULED", "TIMED"]:
        return JsonResponse(
            {"error": "Cannot predict on completed fixtures"}, status=400
        )

    if request.method == "POST":
        form = PredictionForm(request.POST)
        if form.is_valid():
            prediction, created = Prediction.objects.update_or_create(
                user=request.user,
                fixture=fixture,
                defaults={
                    "home_score": form.cleaned_data["home_score"],
                    "away_score": form.cleaned_data["away_score"],
                },
            )
            context = {
                "fixture": fixture,
                "prediction": prediction,
                "can_predict": True,
                "just_updated": True,
            }
            return render(request, "core/prediction_form.html", context)
    return JsonResponse({"error": "Invalid request"}, status=400)
