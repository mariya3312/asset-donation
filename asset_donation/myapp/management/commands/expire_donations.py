from datetime import timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from myapp.models import Donation


class Command(BaseCommand):
    help = "Automatically mark available donations older than 7 days as Expired"

    def handle(self, *args, **options):
        limit = timezone.now() - timedelta(days=7)

        donations = Donation.objects.filter(
            status="Available",
            created_at__lt=limit
        )

        count = donations.count()

        for donation in donations:
            donation.status = "Expired"
            donation.save()

        self.stdout.write(self.style.SUCCESS(f"Expired {count} donations"))
