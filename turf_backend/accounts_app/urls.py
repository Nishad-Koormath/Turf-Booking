from django.urls import path
from .views import RegisterView, LoginView, LogoutView, GetUserByIdView


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('user/<int:user_id>/', GetUserByIdView.as_view(), name='get_user_by_id'),
]