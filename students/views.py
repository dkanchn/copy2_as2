from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Course, QuotaRequest

@login_required
def dashboard(request):
    courses = Course.objects.all()
    quota_requests = QuotaRequest.objects.filter(student=request.user)
    return render(request, 'students/dashboard.html', {'courses': courses, 'quota_requests': quota_requests})

@login_required
def request_quota(request, course_id):
    course = Course.objects.get(id=course_id)
    quota_request = QuotaRequest.objects.create(student=request.user, course=course)
    return redirect('student_dashboard')


@login_required
def student_dashboard(request):
    # แสดงวิชาที่เปิดให้ขอโควต้า
    return render(request, 'students/dashboard.html')
