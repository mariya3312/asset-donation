from django.urls import path
from.import views
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.views import TokenRefreshView
from .views import DonationCreateView

@extend_schema_view(
    post=extend_schema(
        tags=["TOKEN"],
        summary="Refresh Token",
        request=TokenRefreshSerializer,
        responses=TokenRefreshSerializer,
    )
)
class TaggedTokenRefreshView(TokenRefreshView):
    pass

urlpatterns = [

 path('auth/register/', views.RegisterView.as_view(), name='register'),
 path('auth/login/', views.LoginView.as_view(), name='login'),
 path('auth/logout/', views.LogoutView.as_view(), name='logout'),
 path("change-password/", views.ChangePasswordView.as_view(), name="change-password"),
 path("token/refresh/", TaggedTokenRefreshView.as_view(), name="token_refresh"),
  path("auth/forgot-password/", views.ForgotPasswordView.as_view(), name="forgot-password"),
  path("auth/verify-otp/", views.VerifyOTPView.as_view(), name="verify-otp"),
  path("auth/reset-password/", views.ResetPasswordView.as_view(), name="reset-password"),
  path("categories/", views.CategoryListView.as_view(), name="categories"),
   path("donations/", DonationCreateView.as_view(), name="donation-create"),

 path(
        "donations/search/",
        views.DonationSearchView.as_view(),
        name="donation-search",
    ),
     path(
        "donations/nearby/",
        views.NearbyDonationAPIView.as_view(),
        name="nearby-donations"
    ),
   path(
    "donations/<int:id>/images/",
   views. DonationImageUploadView.as_view(),
    name="donation-image-upload"
),
 path(
        "donations/<int:id>/",
        views.DonationDetailView.as_view(),
        name="donation-detail"
    ),
]

