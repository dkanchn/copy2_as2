from django.urls import path
from .views import login_view
from . import views

urlpatterns = [
    path('login/', login_view, name='login'),
    path('login/', views.LoginView.as_view(), name='login'),
    # สามารถเพิ่มเส้นทางอื่น ๆ ที่จำเป็นได้ที่นี่
]
