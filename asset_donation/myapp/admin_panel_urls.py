from django.urls import path
# pyrefly: ignore [missing-import]
from . import admin_panel_views as views

urlpatterns = [
    path('', views.dashboard_view, name='admin_dashboard'),
    path('users/', views.users_view, name='admin_users'),
    path('donations/', views.donations_view, name='admin_donations'),
    path('categories/', views.categories_view, name='admin_categories'),
    path('requests/', views.requests_view, name='admin_requests'),
    path('verification/', views.verification_view, name='admin_verification'),
    path('reports/', views.reports_view, name='admin_reports'),
    path('subscriptions/', views.subscriptions_view, name='admin_subscriptions'),
    path('logout/', views.admin_logout_view, name='admin_logout'),
    path(
        'admin-panel/users/add/',
        views.add_user,
        name='admin_add_user'
    ),
]
