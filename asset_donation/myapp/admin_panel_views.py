from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.db.models import Count, Q
from .models import Donation, Category


def dashboard_view(request):
    total_users = User.objects.count()
    total_donations = Donation.objects.count()
    total_categories = Category.objects.count()

    context = {
        'total_users': total_users,
        'total_donations': total_donations,
        'total_categories': total_categories,
    }
    return render(request, 'admin_panel/dashboard.html', context)


def users_view(request):
    search_query = request.GET.get('q', '').strip()
    role_filter = request.GET.get('role', '').strip()
    status_filter = request.GET.get('status', '').strip()

    users_qs = User.objects.annotate(
        donations_count=Count('donations', distinct=True),
        requests_count=Count('asset_requests', distinct=True)
    )

    if search_query:
        users_qs = users_qs.filter(
            Q(username__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query)
        )

    if role_filter == 'admin':
        users_qs = users_qs.filter(is_superuser=True)
    elif role_filter == 'staff':
        users_qs = users_qs.filter(is_staff=True, is_superuser=False)
    elif role_filter == 'user':
        users_qs = users_qs.filter(is_staff=False, is_superuser=False)

    if status_filter == 'active':
        users_qs = users_qs.filter(is_active=True)
    elif status_filter == 'inactive':
        users_qs = users_qs.filter(is_active=False)

    users = users_qs.order_by('-date_joined')

    context = {
        'users': users,
        'total_users_count': User.objects.count(),
        'active_users_count': User.objects.filter(is_active=True).count(),
        'staff_users_count': User.objects.filter(is_staff=True).count(),
        'search_query': search_query,
        'role_filter': role_filter,
        'status_filter': status_filter,
        'page_title': 'User Management',
    }
    return render(request, 'admin_panel/users.html', context)


def donations_view(request):
    donations = Donation.objects.all()
    return render(request, 'admin_panel/dashboard.html', {'donations': donations, 'page_title': 'Donations Management'})


def categories_view(request):
    categories = Category.objects.all()
    return render(request, 'admin_panel/dashboard.html', {'categories': categories, 'page_title': 'Categories Management'})


def requests_view(request):
    return render(request, 'admin_panel/dashboard.html', {'page_title': 'Requests Management'})


def verification_view(request):
    return render(request, 'admin_panel/dashboard.html', {'page_title': 'Verification Requests'})


def reports_view(request):
    return render(request, 'admin_panel/dashboard.html', {'page_title': 'Reports & Analytics'})


def subscriptions_view(request):
    return render(request, 'admin_panel/dashboard.html', {'page_title': 'Subscriptions'})


def admin_logout_view(request):
    logout(request)
    return redirect('home')
