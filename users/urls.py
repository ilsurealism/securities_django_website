from django.urls import path
from .views import UserLoginView, UserLogoutView, profile, ChangeUserInfoView, UserPasswordChangeVeiw, RegisterUserView, RegisterDoneView
from .views import DeleteUserView, ProfileView, PrivacyView


app_name = 'users'

urlpatterns = [
    path('accounts/login/', UserLoginView.as_view(), name='login'),
    # path('profile/<int:pk>', ProfileView.as_view(), name='profile'),
    # path('profile/<slug:slug>', ProfileView.as_view(), name='profile'),
    # path('accounts/profile/<username>/', ProfileView.as_view(), name='profile'),
    path('accounts/profile/delete/', DeleteUserView.as_view(), name='profile_delete'),
    path('accounts/profile/change/', ChangeUserInfoView.as_view(), name='profile_change'),
    path('accounts/profile/<username>/', ProfileView.as_view(), name='profile_view'),
    path('accounts/profile/', profile, name='profile'),
    path('accounts/logout/', UserLogoutView.as_view(), name='logout'),
    path('accounts/password/change/', UserPasswordChangeVeiw.as_view(), name='password_change'),
    path('accounts/register/done/', RegisterDoneView.as_view(), name='register_done'),
    path('accounts/register/', RegisterUserView.as_view(), name='register'),
    path('privacy', PrivacyView.as_view(), name='privacy')
]