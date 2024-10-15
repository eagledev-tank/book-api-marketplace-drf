# from rest_framework.routers import SimpleRouter
# from .views import UserModelViewSet, ProfileModelViewSet
# from django.urls import path, include
#
#
# router = SimpleRouter()
#
# router.register('User', UserModelViewSet, basename='user')
# router.register('Profile', ProfileModelViewSet, basename='profile')
#
# urlpatterns = [
# ]

from django.urls import path
from .views import (
    RegisterView, LoginView, ProfileView,
    PasswordResetView, PasswordResetConfirmView, ActivateAccountView,
    LogoutView, ProfileUpdateView
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('activation/<str:id>/<str:token>/', ActivateAccountView.as_view(), name='activate'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('password_reset/', PasswordResetView.as_view(), name='password-reset'),
    path('password_reset_confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='activate'),
    path('Profile/Update/', ProfileUpdateView.as_view(), name='profile-update'),
]
