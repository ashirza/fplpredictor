from httpx import Client
from django.core.cache import cache
from fplpredictor import settings
from .models import Fixture


class FplClient:
    base_url = "http://api.football-data.org/v4/"

    def __init__(self):
        self.client = Client()
        self.client.headers["X-Auth-Token"] = settings.FPL_API_KEY

    def get_current_gameweek(self):
        cache_key = "current_gameweek"
        cached_result = cache.get(cache_key)

        if cached_result is not None:
            return cached_result

        response = self.client.get(self.base_url + "competitions/PL/")
        response.raise_for_status()
        result = response.json()["currentSeason"]["currentMatchday"]

        cache.set(cache_key, result, timeout=3600)  # Cache for 1 hour
        return result

    def get_premier_league_id(self):
        cache_key = "premier_league_id"
        cached_result = cache.get(cache_key)

        if cached_result is not None:
            return cached_result

        response = self.client.get(self.base_url + "competitions/PL")
        response.raise_for_status()
        result = response.json()["id"]

        cache.set(cache_key, result, timeout=3600)  # Cache for 1 hour
        return result

    def get_fixtures(self, gameweek=None):
        if gameweek is None:
            gameweek = self.get_current_gameweek()

        response = self.client.get(
            self.base_url + "competitions/PL/matches",
            params={"matchday": gameweek},
        )
        response.raise_for_status()

        fixtures = []
        for match in response.json()["matches"]:
            fixtures.append(
                {
                    "id": match["id"],
                    "home_team": {
                        "id": match["homeTeam"]["id"],
                        "name": match["homeTeam"]["name"],
                        "crest": match["homeTeam"]["crest"],
                    },
                    "away_team": {
                        "id": match["awayTeam"]["id"],
                        "name": match["awayTeam"]["name"],
                        "crest": match["awayTeam"]["crest"],
                    },
                    "status": match["status"],
                    "kickoff": match["utcDate"],
                    "score": {
                        "fullTime": {
                            "home": match["score"]["fullTime"]["home"]
                            if match["status"] == "FINISHED"
                            else None,
                            "away": match["score"]["fullTime"]["away"]
                            if match["status"] == "FINISHED"
                            else None,
                        }
                    },
                }
            )

        return fixtures

    def sync_fixtures(self):
        current_gameweek = self.get_current_gameweek()

        # Get both current and next gameweek fixtures
        gameweeks_to_sync = [current_gameweek]
        if current_gameweek < 38:  # Premier League has 38 gameweeks
            gameweeks_to_sync.append(current_gameweek + 1)

        for gameweek in gameweeks_to_sync:
            fixtures = self.get_fixtures(gameweek=gameweek)

            for fixture in fixtures:
                Fixture.objects.update_or_create(
                    external_id=fixture["id"],
                    defaults={
                        "home_team": fixture["home_team"]["name"],
                        "home_team_crest": fixture["home_team"]["crest"],
                        "away_team": fixture["away_team"]["name"],
                        "away_team_crest": fixture["away_team"]["crest"],
                        "kickoff": fixture["kickoff"],
                        "gameweek": gameweek,
                        "status": fixture["status"],
                        "home_score": fixture["score"]["fullTime"]["home"],
                        "away_score": fixture["score"]["fullTime"]["away"],
                    },
                )
