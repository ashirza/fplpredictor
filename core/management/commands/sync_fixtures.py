from django.core.management.base import BaseCommand
from core.fpl_client import FplClient


class Command(BaseCommand):
    help = "Syncs fixtures from the Football Data API"

    def handle(self, *args, **options):
        client = FplClient()
        client.sync_fixtures()
        self.stdout.write(self.style.SUCCESS("Successfully synced fixtures"))
