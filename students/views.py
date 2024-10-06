from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Course, QuotaRequest
from .forms import CourseForm

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

from django.shortcuts import render, redirect
from .models import Course, QuotaRequest
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    courses = Course.objects.all()
    for course in courses:
        course.available_seats = course.seats - QuotaRequest.objects.filter(course=course, status='approved').count()
    return render(request, 'students/dashboard.html', {'courses': courses})

@login_required
def request_quota(request, course_id):
    if request.method == 'POST':
        course = Course.objects.get(id=course_id)
        QuotaRequest.objects.create(student=request.user, course=course)
        return redirect('student_dashboard')
    return redirect('student_dashboard')

@login_required
def add_course(request):
    if request.method == "POST":
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('student_dashboard')  # เปลี่ยนไปยังหน้าที่คุณต้องการหลังจากบันทึกสำเร็จ
    else:
        form = CourseForm()
    return render(request, 'students/add_course.html', {'form': form})

@login_required
def request_quota(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    # ตรวจสอบว่ามีที่นั่งว่างอยู่หรือไม่
    if course.available_seats > 0:
        # สร้างขอโควต้าใหม่
        quota_request = QuotaRequest(student=request.user, course=course)
        quota_request.save()
        # ปรับปรุงจำนวนที่นั่งว่าง
        course.available_seats -= 1
        course.save()
        return redirect('student_dashboard')  # กลับไปที่แดชบอร์ด
    return redirect('student_dashboard')  # หากไม่สามารถขอโควต้าได้ ให้กลับไปที่แดชบอร์ด

@login_required
def cancel_quota(request, quota_id):
    quota_request = get_object_or_404(QuotaRequest, id=quota_id, student=request.user)
    # ปรับปรุงจำนวนที่นั่งว่างของวิชาที่ถูกยกเลิก
    course = quota_request.course
    course.available_seats += 1
    course.save()
    # ลบขอโควต้า
    quota_request.delete()
    return redirect('student_dashboard')  # กลับไปที่แดชบอร์ด