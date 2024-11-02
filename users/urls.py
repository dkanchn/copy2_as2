from django.urls import path
from .views import login_view
from . import views

urlpatterns = [
    path('login/', login_view, name='login'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('approve/', views.approve_quota_requests, name='approve_quota_requests'),
    path('manage/', views.manage_quota_requests, name='manage_quota_requests'),
]