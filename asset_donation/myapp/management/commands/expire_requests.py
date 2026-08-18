from datetime import timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from myapp.models import Request


class Command(BaseCommand):
    help = "Automatically mark pending donation requests older than 24 hours as Expired"

    def handle(self, *args, **options):
        limit = timezone.now() - timedelta(hours=24)

        requests = Request.objects.filter(
            status="Pending",
            requested_at__lt=limit
        )

        count = requests.count()

        for request in requests:
            request.status = "Expired"
            request.save()

        self.stdout.write(self.style.SUCCESS(f"Expired {count} pending requests"))
