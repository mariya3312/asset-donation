from django.http import request
from django.contrib.auth import base_user
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView

class IndexView(TemplateView):
    template_name = 'index.html'

from django.contrib.auth.models import User
from rest_framework import serializers, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
import random
import math
from .serializers import CategorySerializer, DonationSerializer, DonationImageSerializer
from .models import Category, SubCategory, Donation, DonationImage
from rest_framework.generics import ListAPIView
from django.db.models import Q
from django.core.mail import send_mail
from django.conf import settings
from django.core.exceptions import FieldError
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from drf_spectacular.utils import (
    OpenApiParameter,
    OpenApiResponse,
    OpenApiTypes,
    extend_schema,
    extend_schema_view,
    inline_serializer,
)
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.shortcuts import render
# pyrefly: ignore [missing-import]
from .models import (
    Donation,
    Request,
    Report,
)

class RegisterView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        tags=["AUTH"],
        summary="Register",
        request=inline_serializer(
            name="RegisterRequest",
            fields={
                "full_name": serializers.CharField(),
                "email": serializers.EmailField(),
                "password": serializers.CharField(write_only=True),
            },
        ),
        responses=OpenApiResponse(description="Registration successful"),
    )
    def post(self, request):
        full_name = request.data.get("full_name")
        email = request.data.get("email")
        password = request.data.get("password")

        if not full_name or not email or not password:
            return Response(
                {"error": "All fields are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if User.objects.filter(email=email).exists():
            return Response(
                {"error": "Email already exists."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Create user
        user = User.objects.create_user(
            username=email,
            first_name=full_name,
            email=email,
            password=password
        )

        # Generate JWT Tokens
        refresh = RefreshToken.for_user(user)
        access = refresh.access_token

        return Response(
            {
                "message": "Registration successful",

                "user": {
                    "id": user.id,
                    "full_name": user.first_name,
                    "email": user.email,
                },

                "access": str(access),
                "refresh": str(refresh),
            },
            status=status.HTTP_201_CREATED
        )

        
class LoginView(APIView):

    permission_classes = [AllowAny]

    @extend_schema(
        tags=["AUTH"],
        summary="Login",
        request=inline_serializer(
            name="LoginRequest",
            fields={
                "email": serializers.EmailField(),
                "password": serializers.CharField(write_only=True),
            },
        ),
        responses=OpenApiResponse(description="Login successful"),
    )
    def post(self, request):

        # Get email and password from request
        email = request.data.get("email")
        password = request.data.get("password")

        # Check if email and password are provided
        if not email or not password:
            return Response(
                {"error": "Email and Password are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Authenticate user
        user = authenticate(
            username=email,
            password=password
        )

        # Invalid credentials
        if user is None:
            return Response(
                {"error": "Invalid email or password."},
                status=status.HTTP_401_UNAUTHORIZED
            )

        # Generate Refresh Token
        refresh = RefreshToken.for_user(user)

        # Generate Access Token
        access = refresh.access_token

        # Return response
        return Response(
            {
                "message": "Login Successful",

                "user": {
                    "id": user.id,
                    "full_name": user.first_name,
                    "email": user.email
                },

                "access": str(access),

                "refresh": str(refresh)

            },
            status=status.HTTP_200_OK
        )
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=["AUTH"],
        summary="Logout",
        request=inline_serializer(
            name="LogoutRequest",
            fields={
                "refresh": serializers.CharField(),
            },
        ),
        responses=OpenApiResponse(description="Logout successful"),
    )
    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")

            if not refresh_token:
                return Response(
                    {"error": "Refresh token is required"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(
                {"message": "Logout successful"},
                status=status.HTTP_200_OK
            )

        except Exception:
            return Response(
                {"error": "Invalid refresh token"},
                status=status.HTTP_400_BAD_REQUEST
            )

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user

        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")

        if not user.check_password(old_password):
            return Response(
                {"error": "Old password is incorrect."},
                status=status.HTTP_400_BAD_REQUEST
            )

        user.set_password(new_password)
        user.save()

        return Response(
            {"message": "Password changed successfully."},
            status=status.HTTP_200_OK
        )
class TokenRefreshAPIView(APIView):
    permission_classes = []

    def post(self, request):
        refresh_token = request.data.get("refresh")

        if not refresh_token:
            return Response(
                {"error": "Refresh token is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            refresh = RefreshToken(refresh_token)

            return Response(
                {
                    "access": str(refresh.access_token)
                },
                status=status.HTTP_200_OK
            )

        except TokenError:
            return Response(
                {"error": "Refresh token is invalid or expired."},
                status=status.HTTP_401_UNAUTHORIZED
            )
class ForgotPasswordView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        tags=["AUTH"],
        summary="Forgot Password",
        request=inline_serializer(
            name="ForgotPasswordRequest",
            fields={
                "email": serializers.EmailField(),
            },
        ),
        responses=OpenApiResponse(description="OTP sent successfully"),
    )
    def post(self, request):
        email = request.data.get("email")

        if not email:
            return Response(
                {"error": "Email is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {"error": "User not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        # Generate 6-digit OTP
        otp = random.randint(100000, 999999)

        # Save OTP (for demo only)
        user.last_name = str(otp)
        user.save()

        # Send OTP via email
        try:
            send_mail(
                subject="Your Password Reset OTP",
                message=f"Hello,\n\nYour OTP for resetting your password is: {otp}\n\nIf you did not request this, please ignore this email.",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=False,
            )
        except Exception as e:
            return Response(
                {
                    "error": f"Failed to send OTP email: {str(e)}",
                    "otp": otp
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return Response(
            {
                "message": "OTP sent successfully to your email.",
                "otp": otp
            },
            status=status.HTTP_200_OK
        )


class VerifyOTPView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        tags=["AUTH"],
        summary="Verify OTP",
        request=inline_serializer(
            name="VerifyOTPRequest",
            fields={
                "email": serializers.EmailField(),
                "otp": serializers.CharField(),
            },
        ),
        responses=OpenApiResponse(description="OTP verified successfully"),
    )
    def post(self, request):
        email = request.data.get("email")
        otp = request.data.get("otp")

        if not email or not otp:
            return Response(
                {"error": "Email and OTP are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {"error": "User not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        if user.last_name != str(otp):
            return Response(
                {"error": "Invalid or expired OTP."},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {"message": "OTP verified successfully."},
            status=status.HTTP_200_OK
        )


class ResetPasswordView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        tags=["AUTH"],
        summary="Reset Password",
        request=inline_serializer(
            name="ResetPasswordRequest",
            fields={
                "email": serializers.EmailField(),
                "otp": serializers.CharField(),
                "new_password": serializers.CharField(write_only=True),
                "confirm_password": serializers.CharField(write_only=True),
            },
        ),
        responses=OpenApiResponse(description="Password reset successfully"),
    )
    def post(self, request):
        email = request.data.get("email")
        otp = request.data.get("otp")
        new_password = request.data.get("new_password")
        confirm_password = request.data.get("confirm_password")

        if not email or not otp or not new_password or not confirm_password:
            return Response(
                {"error": "Email, OTP, new_password, and confirm_password are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if new_password != confirm_password:
            return Response(
                {"error": "New password and confirm password do not match."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {"error": "User not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        if user.last_name != str(otp):
            return Response(
                {"error": "Invalid or expired OTP."},
                status=status.HTTP_400_BAD_REQUEST
            )

        user.set_password(new_password)
        user.last_name = ""  # Clear OTP after successful reset
        user.save()

        return Response(
            {"message": "Password reset successfully."},
            status=status.HTTP_200_OK
        )

    
class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=["PASSWORD"],
        summary="Change Password",
        request=inline_serializer(
            name="ChangePasswordRequest",
            fields={
                "old_password": serializers.CharField(write_only=True),
                "new_password": serializers.CharField(write_only=True),
                "confirm_password": serializers.CharField(write_only=True),
            },
        ),
        responses=OpenApiResponse(description="Password changed successfully"),
    )
    def post(self, request):

        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")
        confirm_password = request.data.get("confirm_password")

        # Check required fields
        if not old_password or not new_password or not confirm_password:
            return Response(
                {"error": "All fields are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check old password
        if not request.user.check_password(old_password):
            return Response(
                {"error": "Old password is incorrect."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check new password confirmation
        if new_password != confirm_password:
            return Response(
                {"error": "New password and confirm password do not match."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Update password
        request.user.set_password(new_password)
        request.user.save()

        return Response(
            {
                "message": "Password changed successfully."
            },
            status=status.HTTP_200_OK
        )
class CategoryListView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        tags=["CATEGORIES"],
        summary="Categories",
        responses=CategorySerializer(many=True),
    )
    def get(self, request):
        categories = Category.objects.prefetch_related("subcategories").all()

        serializer = CategorySerializer(
            categories,
            many=True,
            context={"request": request}
        )

        return Response(serializer.data, status=status.HTTP_200_OK)

class DonationCreateView(APIView):
    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated()]
        return [AllowAny()]

    @extend_schema(
        tags=["DONATIONS"],
        summary="List Donations",
        responses=DonationSerializer(many=True),
    )
    def get(self, request):
        donations = Donation.objects.all().order_by("-created_at")
        serializer = DonationSerializer(donations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        tags=["DONATIONS"],
        summary="Create Donation",
        request=DonationSerializer,
        responses=DonationSerializer,
    )
    def post(self, request):
        serializer = DonationSerializer(data=request.data)

        if serializer.is_valid():
            donation = serializer.save(user=request.user)

            return Response(
                {
                    "message": "Donation created successfully",
                    "data": DonationSerializer(donation).data
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )



@extend_schema_view(
    get=extend_schema(
        tags=["DONATIONS"],
        summary="Search Donations",
        parameters=[
            OpenApiParameter("q", OpenApiTypes.STR, OpenApiParameter.QUERY),
            OpenApiParameter("category", OpenApiTypes.INT, OpenApiParameter.QUERY),
            OpenApiParameter("subcategory", OpenApiTypes.INT, OpenApiParameter.QUERY),
            OpenApiParameter("condition", OpenApiTypes.STR, OpenApiParameter.QUERY),
            OpenApiParameter("status", OpenApiTypes.STR, OpenApiParameter.QUERY),
            OpenApiParameter("urgency", OpenApiTypes.STR, OpenApiParameter.QUERY),
            OpenApiParameter("city", OpenApiTypes.STR, OpenApiParameter.QUERY),
            OpenApiParameter("ordering", OpenApiTypes.STR, OpenApiParameter.QUERY),
        ],
        responses=DonationSerializer(many=True),
    )
)
class DonationSearchView(ListAPIView):
    serializer_class = DonationSerializer

    def get_queryset(self):
        queryset = Donation.objects.all()

        q = self.request.query_params.get("q")
        category = self.request.query_params.get("category")
        subcategory = self.request.query_params.get("subcategory")
        condition = self.request.query_params.get("condition")
        status = self.request.query_params.get("status")
        urgency = self.request.query_params.get("urgency")
        city = self.request.query_params.get("city")

        if q:
            queryset = queryset.filter(
                Q(title__icontains=q) |
                Q(description__icontains=q)
            )

        if category:
            queryset = queryset.filter(
                subcategory__category_id=category
            )

        if subcategory:
            queryset = queryset.filter(
                subcategory_id=subcategory
            )

        if condition:
            queryset = queryset.filter(
                condition__iexact=condition
            )

        if status:
            queryset = queryset.filter(
                status__iexact=status
            )

        if urgency:
            queryset = queryset.filter(
                urgency__iexact=urgency
            )

        if city:
            queryset = queryset.filter(
                pickup_location__icontains=city
            )

        ordering = self.request.query_params.get("ordering")

        if ordering:
            try:
                queryset = queryset.order_by(ordering)
            except FieldError:
                queryset = queryset.order_by("-created_at")
        else:
            queryset = queryset.order_by("-created_at")

        return queryset

    
def haversine_km(lat1, lon1, lat2, lon2):
    R = 6371.0  # Earth's radius in km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(math.radians(lat1))
        * math.cos(math.radians(lat2))
        * math.sin(dlon / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


class NearbyDonationAPIView(APIView):

    @extend_schema(
        tags=["DONATIONS"],
        summary="Nearby Donations",
        parameters=[
            OpenApiParameter("latitude", OpenApiTypes.FLOAT, OpenApiParameter.QUERY, required=True),
            OpenApiParameter("longitude", OpenApiTypes.FLOAT, OpenApiParameter.QUERY, required=True),
            OpenApiParameter("radius", OpenApiTypes.FLOAT, OpenApiParameter.QUERY),
        ],
        responses=DonationSerializer(many=True),
    )
    def get(self, request):
        lat_param = request.GET.get("latitude")
        lon_param = request.GET.get("longitude")
        radius_param = request.GET.get("radius", 3)

        if not lat_param or not lon_param:
            return Response(
                {"error": "Both 'latitude' and 'longitude' query parameters are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            latitude = float(lat_param)
            longitude = float(lon_param)
            radius = float(radius_param)
        except (ValueError, TypeError):
            return Response(
                {"error": "Invalid numeric value for latitude, longitude, or radius."},
                status=status.HTTP_400_BAD_REQUEST
            )

        nearby = []
        donations = Donation.objects.filter(status="Available")

        for donation in donations:
            if donation.latitude is not None and donation.longitude is not None:
                try:
                    don_lat = float(donation.latitude)
                    don_lon = float(donation.longitude)
                except (ValueError, TypeError):
                    continue

                distance = haversine_km(latitude, longitude, don_lat, don_lon)

                if distance <= radius:
                    data = DonationSerializer(donation).data
                    data["distance"] = round(distance, 2)
                    nearby.append(data)

        nearby = sorted(nearby, key=lambda x: x["distance"])
        return Response(nearby, status=status.HTTP_200_OK)


class DonationImageUploadView(APIView):

    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=["DONATIONS"],
        summary="Upload Donation Images",
        request={
            "multipart/form-data": inline_serializer(
                name="DonationImageUploadRequest",
                fields={
                    "image": serializers.ImageField(),
                    "is_primary": serializers.BooleanField(required=False),
                },
            )
        },
        responses=DonationImageSerializer,
    )
    def post(self, request, id):

        donation = get_object_or_404(
            Donation,
            id=id
        )

        image = request.FILES.get("image")

        if not image:
            return Response(
                {"error": "Image is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        donation_image = DonationImage.objects.create(
            donation=donation,
            image=image,
            is_primary=request.data.get("is_primary", False)
        )

        serializer = DonationImageSerializer(donation_image)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )

class DonationDetailView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=["DONATIONS"],
        summary="Donation Detail",
        responses=DonationSerializer,
    )
    def get(self, request, id):
        donation = get_object_or_404(Donation, id=id)
        serializer = DonationSerializer(donation)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        tags=["DONATIONS"],
        summary="Update Donation",
        request=DonationSerializer,
        responses=DonationSerializer,
    )
    def put(self, request, id):
        donation = get_object_or_404(Donation, id=id)

        # Check ownership
        if donation.user != request.user:
            return Response(
                {"detail": "You can only update your own donation."},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = DonationSerializer(
            donation,
            data=request.data
        )

        if serializer.is_valid():
            serializer.save()

            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    @extend_schema(
        tags=["DONATIONS"],
        summary="Partial Update",
        request=DonationSerializer,
        responses=DonationSerializer,
    )
    def patch(self, request, id):
        donation = get_object_or_404(Donation, id=id)

        if donation.user != request.user:
            return Response(
                {"detail": "You can only update your own donation."},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = DonationSerializer(
            donation,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            serializer.save()

            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    @extend_schema(
        tags=["DONATIONS"],
        summary="Delete Donation",
        responses=OpenApiResponse(description="Donation deleted successfully"),
    )
    def delete(self, request, id):
        donation = get_object_or_404(Donation, id=id)

        if donation.user != request.user:
            return Response(
                {"detail": "You can only delete your own donation."},
                status=status.HTTP_403_FORBIDDEN
            )

        donation.delete()
        return Response(
            {"message": "Donation deleted successfully."},
            status=status.HTTP_204_NO_CONTENT
        )
class DonationListView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        donations = Donation.objects.all()

        serializer = DonationSerializer(
            donations,
            many=True
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )
    def dashboard(request):

    # pyrefly: ignore [parse-error]
    context = {
        'total_users': User.objects.count(),

        'total_donations':
            Donation.objects.count(),

        'total_requests':
            Request.objects.count(),

        'total_reports':
            Report.objects.count(),

        'recent_donations':
            Donation.objects.order_by(
                '-created_at'
            )[:10],
    }

    # pyrefly: ignore [invalid-syntax]
    return render(
        request,
        'myapp/dashboard.html',
        context
    )
  
