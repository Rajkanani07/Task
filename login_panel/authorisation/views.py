from django.utils import timezone
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User_Details
from django.db.models import Q
# from django.contrib.auth import logout
from django.contrib.auth import login as auth_login, logout as auth_logout
from .serializers import (
    UserSerializer, 
    UserCreateSerializer, 
    LoginSerializer, 
)

MAX_FAILED_ATTEMPTS = 3
BLOCK_DURATION = timezone.timedelta(minutes=1)

class UserListApiView(APIView):
    permission_classes = [permissions.AllowAny]

    # POST Method
    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # GET Method
    def get(self, request, *args, **kwargs):
        username = request.query_params.get('username')
        if username:
            users = User_Details.objects.filter(username=username)
            if users.exists():
                serializer = UserSerializer(users, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"error": "No users found with the provided username"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"error": "Please provide a username query parameter"}, status=status.HTTP_400_BAD_REQUEST)

    # PUT Method
    def put(self, request, *args, **kwargs):
        username = request.query_params.get('username')
        if username:
            try:
                user = User_Details.objects.get(username=username)
                serializer = UserSerializer(user, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response({"message": "User updated successfully"}, status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except User_Details.DoesNotExist:
                return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response({"error": "Please provide a username query parameter"}, status=status.HTTP_400_BAD_REQUEST)

    # DELETE Method
    def delete(self, request, *args, **kwargs):
        username = request.query_params.get('username')
        if username:
            try:
                user = User_Details.objects.get(username=username)
                user.delete()
                return Response({"message": "User deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
            except User_Details.DoesNotExist:
                return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response({"error": "Please provide a username query parameter"}, status=status.HTTP_400_BAD_REQUEST)\
        

class LoginAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            identifier = serializer.validated_data.get("identifier")
            password = serializer.validated_data.get("password")
            user = None
            try:
                if '@' in identifier:
                    user = User_Details.objects.get(email_id=identifier)
                else:
                    user = User_Details.objects.get(username=identifier)
                # user = User_Details.objects.get(Q(email_id=identifier) | Q(username=identifier))
            except User_Details.DoesNotExist:
                return Response(
                    {"error": "Invalid credentials"},
                    status=status.HTTP_401_UNAUTHORIZED,
                )

            if user.is_user_login:
                return Response(
                    {"error": "User is already logged in."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            
            if user and user.is_password_valid(password):
                if user.block_expiration and user.block_expiration > timezone.now():
                    return Response(
                        {"error": "Account blocked. Please try again later."},
                        status=status.HTTP_401_UNAUTHORIZED,
                    )
                user.unsuccessful_attempts = 0
                user.block_expiration = None
                user.is_user_login = True
                user.save()
                auth_login(request, user)
                return Response(
                    {"message": "Login successful"}, status=status.HTTP_200_OK
                )
            else:
                user.unsuccessful_attempts += 1
                user.last_login_attempt = timezone.now()
                if user.unsuccessful_attempts >= MAX_FAILED_ATTEMPTS:
                    user.block_expiration = timezone.now() + BLOCK_DURATION
                user.save()
                if user.block_expiration and user.block_expiration > timezone.now():
                    return Response(
                        {"error": "Account blocked. Please try again later."},
                        status=status.HTTP_401_UNAUTHORIZED,
                    )
                else:
                    return Response(
                        {"error": "Invalid credentials"},
                        status=status.HTTP_401_UNAUTHORIZED,
                    )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class LogoutAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        # Check if the session exists (user is logged in)
        if request.session.exists(request.session.session_key):
            # Clear the session data manually
            request.session.flush()
            
            # Set is_user_login to False in the database
            user = request.user  # Assuming request.user is set correctly after authentication
            auth_logout(request, user)
            if user.is_authenticated:
                user.is_user_login = False
                user.save()
                # auth_logout(request, user)
            
            return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Not logged in"}, status=status.HTTP_400_BAD_REQUEST)
        

# class LogoutAPIView(APIView):
#     permission_classes = [permissions.AllowAny]

#     def post(self, request):
#         if request.user.is_authenticated:
#             user = request.user
#             if user.is_user_login:
#                 auth_logout(request)
#                 user.is_user_login = False
#                 user.save()
#                 return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)
#             else:
#                 return Response({"error": "Already logged out"}, status=status.HTTP_400_BAD_REQUEST)
#         else:
#             return Response({"error": "Not logged in"}, status=status.HTTP_400_BAD_REQUEST)


# class LoginAPIView(APIView):
#     permission_classes = [permissions.AllowAny]

#     def post(self, request):
#         serializer = LoginSerializer(data=request.data)
#         if serializer.is_valid():
#             identifier = serializer.validated_data.get("identifier")
#             password = serializer.validated_data.get("password")
#             user = None
#             try:
#                 if '@' in identifier:
#                     user = User_Details.objects.get(email_id=identifier)
#                 else:
#                     user = User_Details.objects.get(username=identifier)
#             except User_Details.DoesNotExist:
#                 return Response(
#                     {"error": "Invalid credentials"},
#                     status=status.HTTP_401_UNAUTHORIZED,
#                 )

#             if user and user.is_password_valid(password):
#                 if user.block_expiration and user.block_expiration > timezone.now():
#                     return Response(
#                         {"error": "Account blocked. Please try again later."},
#                         status=status.HTTP_401_UNAUTHORIZED,
#                     )
#                 user.unsuccessful_attempts = 0
#                 user.block_expiration = None
#                 user.save()
#                 return Response(
#                     {"message": "Login successful"}, status=status.HTTP_200_OK
#                 )
#             else:
#                 user.unsuccessful_attempts += 1
#                 user.last_login_attempt = timezone.now()
#                 if user.unsuccessful_attempts >= MAX_FAILED_ATTEMPTS:
#                     user.block_expiration = timezone.now() + BLOCK_DURATION
#                 user.save()
#                 if user.block_expiration and user.block_expiration > timezone.now():
#                     return Response(
#                         {"error": "Account blocked. Please try again later."},
#                         status=status.HTTP_401_UNAUTHORIZED,
#                     )
#                 else:
#                     return Response(
#                         {"error": "Invalid credentials"},
#                         status=status.HTTP_401_UNAUTHORIZED,
#                     )
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

# class LogoutAPIView(APIView):
#     permission_classes = [permissions.AllowAny]

#     def post(self, request):
#         if request.user.is_authenticated:
#             if not request.session.get('has_logged_out', False):
#                 logout(request)
#                 request.session['has_logged_out'] = True
#                 return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)
#             else:
#                 return Response({"error": "Already logged out"}, status=status.HTTP_400_BAD_REQUEST)
#         else:
#             return Response({"error": "Not logged in"}, status=status.HTTP_400_BAD_REQUEST)


# class LogoutAPIView(APIView):
#     permission_classes = [permissions.AllowAny]

#     def post(self, request):
#         if request.user.is_authenticated:
#             user = request.user
#             if user.is_user_login:
#                 auth_logout(request)
#                 user.is_user_login = False
#                 user.save()
#                 return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)
#             else:
#                 return Response({"error": "Already logged out"}, status=status.HTTP_400_BAD_REQUEST)
#         else:
#             return Response({"error": "Not logged in"}, status=status.HTTP_400_BAD_REQUEST)