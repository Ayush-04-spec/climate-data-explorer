from django.urls import path
from .views import UserRegistrationView, UserLoginView, CustomLogoutView, CustomLogoutSuccessView, HomeView, UserProfileView

app_name = 'users'


urlpatterns= [
    path('', HomeView.as_view(), name='home'),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('logged-out/', CustomLogoutSuccessView.as_view(), name='logged-out'),

]