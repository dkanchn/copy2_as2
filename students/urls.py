from django.urls import path
from .views import dashboard, request_quota

urlpatterns = [
    path('dashboard/', dashboard, name='student_dashboard'),
    path('request_quota/<int:course_id>/', request_quota, name='request_quota'),
]
