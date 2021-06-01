from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path('login/', views.MyLoginView.as_view(), name="login"),
    path('logout/', views.MyLogoutView.as_view(), name="logout"),
    path('signup/', views.SignUpView.as_view(), name="signup"),
    path('profile/', views.ProfileView.as_view(), name="profile"),
]