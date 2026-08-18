from rest_framework import serializers
from .models import Category, SubCategory, ChildCategory, Donation, DonationImage



class ChildCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ChildCategory
        fields = ["id", "name", "image"]


class SubCategorySerializer(serializers.ModelSerializer):
    childcategories = ChildCategorySerializer(many=True, read_only=True)

    class Meta:
        model = SubCategory
        fields = ["id", "name", "childcategories"]


class CategorySerializer(serializers.ModelSerializer):
    subcategories = SubCategorySerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ["id", "name", "description", "subcategories"]

class DonationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donation
        fields = "__all__"
        read_only_fields = ["user"]

class DonationImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = DonationImage
        fields = ["id", "donation", "image", "is_primary", "created_at"]
        read_only_fields = ["id", "donation", "created_at"]
