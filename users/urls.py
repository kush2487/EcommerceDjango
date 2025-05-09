from django.urls import path
from users import views


urlpatterns = [
    path('signUp/', views.registered_user),
]
