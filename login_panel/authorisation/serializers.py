from rest_framework import serializers
from .models import User_Details  # Import your User model
# from django.contrib.auth import get_user_model, authenticate
# from django.contrib.auth.hashers import check_password

from django.utils import timezone

MAX_FAILED_ATTEMPTS = 3
BLOCK_DURATION = timezone.timedelta(minutes=5)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User_Details
        fields = [
            'user_id',
            'first_name',
            'last_name',
            'username',
            'email_id',
            'mobile_number',
            'gender',
            'date_of_birth'
        ]

class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User_Details
        fields = [
            'first_name',
            'last_name',
            'username',
            'email_id',
            'mobile_number',
            'password',
            'gender',
            'date_of_birth'
        ]
        # extra_kwargs = {
        #     'password': {'write_only': True}
        # }


class LoginSerializer(serializers.Serializer):
    identifier = serializers.CharField()
    password = serializers.CharField()



# class LoginSerializer(serializers.Serializer):
#     username = serializers.CharField()
#     email_id = serializers.EmailField()
#     password = serializers.CharField()

# class LoginSerializer(serializers.Serializer):
#     username = serializers.CharField(required=True)
#     password = serializers.CharField(required=True)

#     def validate(self, attrs):
#         username = attrs.get('username')
#         password = attrs.get('password')

#         user_details = User_Details.objects.filter(username=username).first()
#         print(user_details)
#         print(User_Details.objects.filter(username=username).first())
        
#         if user_details is None:
#             raise serializers.ValidationError("User does not exist.")

#         # Check if the account is blocked
#         if user_details.is_blocked:
#             raise serializers.ValidationError("Account blocked. Please try again later.")

#         # Check if the password is correct
#         if not check_password(password, user_details.password):
#             user_details.unsuccessful_attempts += 1
#             user_details.last_login = timezone.now()
#             print(user_details.last_login)
#             if user_details.unsuccessful_attempts >= MAX_FAILED_ATTEMPTS:
#                 user_details.block_expiration = timezone.now() + BLOCK_DURATION
#                 user_details.is_blocked = True  # Mark the account as blocked
#             user_details.save()
#             raise serializers.ValidationError("Invalid username or password.")

#         # Reset unsuccessful attempts on successful login
#         user_details.unsuccessful_attempts = 0
#         user_details.is_blocked = False  # Unblock the user on successful login
#         user_details.block_expiration = None
#         user_details.last_login = timezone.now()
#         user_details.save()

#         attrs['user'] = user_details  # Use user_details instead of user
#         return attrs
    