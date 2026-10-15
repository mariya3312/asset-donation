from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.db.models import Count, Q
# pyrefly: ignore [missing-import]
from .models import Donation, Category, SubCategory, ChildCategory, Request




def dashboard_view(request):
    total_users = User.objects.count()
    total_donations = Donation.objects.count()
    total_categories = Category.objects.count()
    total_requests = Request.objects.count()

    recent_donations = Donation.objects.select_related('user', 'subcategory').prefetch_related('images').order_by('-created_at')[:10]

    context = {
        'total_users': total_users,
        'total_donations': total_donations,
        'total_categories': total_categories,
        'total_requests': total_requests,
        'total_reports': 0,
        'recent_donations': recent_donations,
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
    search_query = request.GET.get('q', '').strip()
    status_filter = request.GET.get('status', '').strip()
    condition_filter = request.GET.get('condition', '').strip()

    donations_qs = Donation.objects.select_related('user', 'subcategory__category').prefetch_related('images')

    if search_query:
        donations_qs = donations_qs.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(pickup_location__icontains=search_query) |
            Q(user__username__icontains=search_query) |
            Q(subcategory__name__icontains=search_query)
        )

    if status_filter:
        donations_qs = donations_qs.filter(status=status_filter)

    if condition_filter:
        donations_qs = donations_qs.filter(condition=condition_filter)

    donations = donations_qs.order_by('-created_at')

    total_donations_count = Donation.objects.count()
    available_count = Donation.objects.filter(status='Available').count()
    reserved_count = Donation.objects.filter(status='Reserved').count()
    completed_count = Donation.objects.filter(status='Completed').count()

    context = {
        'donations': donations,
        'total_donations_count': total_donations_count,
        'available_count': available_count,
        'reserved_count': reserved_count,
        'completed_count': completed_count,
        'search_query': search_query,
        'status_filter': status_filter,
        'condition_filter': condition_filter,
        'page_title': 'Donations Management',
    }
    return render(request, 'admin_panel/donations.html', context)


def categories_view(request):
    category_type = request.GET.get('type', 'main').lower()
    search_query = request.GET.get('q', '').strip()

    total_categories_count = Category.objects.count()
    total_subcategories_count = SubCategory.objects.count()
    total_childcategories_count = ChildCategory.objects.count()
    total_donations_count = Donation.objects.count()

    items = []
    if category_type == 'sub':
        page_title = 'Sub Categories Management'
        sub_qs = SubCategory.objects.select_related('category').annotate(
            child_count=Count('childcategories', distinct=True),
            donations_count=Count('donations', distinct=True)
        )
        if search_query:
            sub_qs = sub_qs.filter(
                Q(name__icontains=search_query) |
                Q(description__icontains=search_query) |
                Q(category__name__icontains=search_query)
            )
        items = sub_qs.order_by('category__name', 'name')
    elif category_type == 'child':
        page_title = 'Child Categories Management'
        child_qs = ChildCategory.objects.select_related('subcategory', 'subcategory__category')
        if search_query:
            child_qs = child_qs.filter(
                Q(name__icontains=search_query) |
                Q(description__icontains=search_query) |
                Q(subcategory__name__icontains=search_query) |
                Q(subcategory__category__name__icontains=search_query)
            )
        items = child_qs.order_by('subcategory__name', 'name')
    else:
        category_type = 'main'
        page_title = 'Main Categories Management'
        categories_qs = Category.objects.annotate(
            subcategories_count=Count('subcategories', distinct=True),
            donations_count=Count('subcategories__donations', distinct=True)
        ).prefetch_related('subcategories')

        if search_query:
            categories_qs = categories_qs.filter(
                Q(name__icontains=search_query) |
                Q(description__icontains=search_query) |
                Q(subcategories__name__icontains=search_query)
            ).distinct()
        items = categories_qs.order_by('name')

    context = {
        'items': items,
        'category_type': category_type,
        'total_categories_count': total_categories_count,
        'total_subcategories_count': total_subcategories_count,
        'total_childcategories_count': total_childcategories_count,
        'total_donations_count': total_donations_count,
        'search_query': search_query,
        'page_title': page_title,
    }
    return render(request, 'admin_panel/categories.html', context)



def requests_view(request):
    return render(request, 'admin_panel/dashboard.html', {'page_title': 'Requests Management'})


def verification_view(request):
    return render(request, 'admin_panel/dashboard.html', {'page_title': 'Verification Requests'})


def reports_view(request):
    return render(request, 'admin_panel/dashboard.html', {'page_title': 'Reports & Analytics'})


def subscriptions_view(request):
    return render(request, 'admin_panel/dashboard.html', {'page_title': 'Subscriptions'})


def add_user(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()
        role = request.POST.get('role', 'user')

        if username and password:
            user = User.objects.create_user(username=username, email=email, password=password)
            if role == 'admin':
                user.is_superuser = True
                user.is_staff = True
            elif role == 'staff':
                user.is_staff = True
            user.save()
    return redirect('admin_users')


def admin_logout_view(request):
    logout(request)
    return redirect('home')
    
def category_add(request):
    category_type = request.GET.get('type', request.POST.get('category_type', 'main')).lower()
    if category_type not in ['main', 'sub', 'child']:
        category_type = 'main'

    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        description = request.POST.get("description", "").strip()

        if category_type == 'sub':
            category_id = request.POST.get("category_id")
            if name and category_id:
                SubCategory.objects.create(
                    category_id=category_id,
                    name=name,
                    description=description
                )
        elif category_type == 'child':
            subcategory_id = request.POST.get("subcategory_id")
            image = request.FILES.get("image")
            if name and subcategory_id:
                ChildCategory.objects.create(
                    subcategory_id=subcategory_id,
                    name=name,
                    description=description,
                    image=image
                )
        else:
            if name:
                Category.objects.create(
                    name=name,
                    description=description
                )

        return redirect(f"/admin-panel/categories/?type={category_type}")

    categories = Category.objects.all().order_by('name')
    subcategories = SubCategory.objects.select_related('category').all().order_by('category__name', 'name')

    type_titles = {
        'main': 'Main Category',
        'sub': 'Sub Category',
        'child': 'Child Category'
    }

    context = {
        'category_type': category_type,
        'page_title': f"Add {type_titles.get(category_type, 'Category')}",
        'categories': categories,
        'subcategories': subcategories,
    }

    return render(
        request,
        "admin_panel/category_add.html",
        context
    )

