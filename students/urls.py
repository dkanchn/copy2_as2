from django.urls import path
from .views import dashboard, request_quota
from .views import add_course
from students import views

urlpatterns = [
    path('dashboard/', dashboard, name='student_dashboard'),
    path('request_quota/<int:course_id>/', request_quota, name='request_quota'),
    path('add-course/', add_course, name='add_course'),
    path('cancel_request/<int:quota_id>/', views.cancel_request, name='cancel_request'),
    path('enroll/<int:course_id>/', views.enroll_course, name='enroll_course'),
]