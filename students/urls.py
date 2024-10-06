from django.urls import path
from .views import dashboard, request_quota, cancel_quota
from .views import add_course

urlpatterns = [
    path('dashboard/', dashboard, name='student_dashboard'),
    path('request_quota/<int:course_id>/', request_quota, name='request_quota'),
    path('add-course/', add_course, name='add_course'),
    path('cancel/<int:quota_id>/', cancel_quota, name='cancel_quota'),
]
