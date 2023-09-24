from django.urls import path, include
from user.views import UserLoginViews, RegistrationViews, ProfileUpdateViews, EmailVerificationViews
from django.contrib.auth.views import LogoutView
from django.contrib.auth.decorators import login_required

app_name = 'users'

urlpatterns = [
    path('login/', UserLoginViews.as_view(), name='login'),
    path('register/', RegistrationViews.as_view(), name='register'),
    path('profile/<int:pk>/', login_required(ProfileUpdateViews.as_view()), name='profile'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('verify/<str:email>/<str:code>/', EmailVerificationViews.as_view(), name='email_verification'),
]
