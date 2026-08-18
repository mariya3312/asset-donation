from datetime import timedelta
from io import StringIO
from django.contrib.auth.models import User
from django.core.management import call_command
from django.test import TestCase
from django.utils import timezone
from myapp.models import Category, SubCategory, Donation, Request


class ExpireRequestsCommandTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="john",
            email="john@example.com",
            password="password123"
        )
        self.category = Category.objects.create(name="Electronics")
        self.subcategory = SubCategory.objects.create(
            category=self.category,
            name="Laptops"
        )
        self.donation = Donation.objects.create(
            user=self.user,
            subcategory=self.subcategory,
            title="Laptop",
            description="Good laptop",
            condition="Good",
            pickup_location="Main Office"
        )

    def test_expire_requests_command(self):
        now = timezone.now()

        # Request 1: Pending, 30 hours old -> Should be Expired
        old_pending_request = Request.objects.create(
            donation=self.donation,
            requester=self.user,
            status="Pending",
            requested_at=now - timedelta(hours=30)
        )

        # Request 2: Pending, 5 hours old -> Should stay Pending
        recent_pending_request = Request.objects.create(
            donation=self.donation,
            requester=self.user,
            status="Pending",
            requested_at=now - timedelta(hours=5)
        )

        # Request 3: Accepted, 40 hours old -> Should stay Accepted
        accepted_request = Request.objects.create(
            donation=self.donation,
            requester=self.user,
            status="Accepted",
            requested_at=now - timedelta(hours=40)
        )

        out = StringIO()
        call_command("expire_requests", stdout=out)

        old_pending_request.refresh_from_db()
        recent_pending_request.refresh_from_db()
        accepted_request.refresh_from_db()

        self.assertEqual(old_pending_request.status, "Expired")
        self.assertEqual(recent_pending_request.status, "Pending")
        self.assertEqual(accepted_request.status, "Accepted")
        self.assertIn("Expired 1 pending requests", out.getvalue())


class ExpireDonationsCommandTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="password123"
        )
        self.category = Category.objects.create(name="Furniture")
        self.subcategory = SubCategory.objects.create(
            category=self.category,
            name="Chairs"
        )

    def test_expire_donations_command(self):
        now = timezone.now()

        # Donation 1: Available, 8 days old -> Should be Expired
        old_available_donation = Donation.objects.create(
            user=self.user,
            subcategory=self.subcategory,
            title="Old Chair",
            description="An old chair",
            condition="Used",
            status="Available",
            pickup_location="Main Office"
        )
        old_available_donation.created_at = now - timedelta(days=8)
        old_available_donation.save()

        # Donation 2: Available, 6 days old -> Should stay Available
        recent_available_donation = Donation.objects.create(
            user=self.user,
            subcategory=self.subcategory,
            title="Recent Chair",
            description="A recent chair",
            condition="Like New",
            status="Available",
            pickup_location="Main Office"
        )
        recent_available_donation.created_at = now - timedelta(days=6)
        recent_available_donation.save()

        # Donation 3: Reserved, 9 days old -> Should stay Reserved
        old_reserved_donation = Donation.objects.create(
            user=self.user,
            subcategory=self.subcategory,
            title="Reserved Chair",
            description="A reserved chair",
            condition="New",
            status="Reserved",
            pickup_location="Main Office"
        )
        old_reserved_donation.created_at = now - timedelta(days=9)
        old_reserved_donation.save()

        out = StringIO()
        call_command("expire_donations", stdout=out)

        old_available_donation.refresh_from_db()
        recent_available_donation.refresh_from_db()
        old_reserved_donation.refresh_from_db()

        self.assertEqual(old_available_donation.status, "Expired")
        self.assertEqual(recent_available_donation.status, "Available")
        self.assertEqual(old_reserved_donation.status, "Reserved")
        self.assertIn("Expired 1 donations", out.getvalue())

