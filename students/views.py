from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Course, QuotaRequest
from .forms import CourseForm
from django.contrib import messages

@login_required
def dashboard(request):
    courses = Course.objects.all()
    quota_requests = QuotaRequest.objects.filter(student=request.user)
    context = {
        'courses': courses,
        'quota_requests': quota_requests,
    }
    return render(request, 'students/dashboard.html', context)

@login_required
def request_quota(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    user = request.user
    
    # ตรวจสอบว่านักเรียนได้ลงทะเบียนในหลักสูตรนี้แล้วหรือไม่
    existing_request = QuotaRequest.objects.filter(course=course, student=user).first()
    
    if not existing_request:
        # สร้างคำขอควอทาสำหรับหลักสูตร
        QuotaRequest.objects.create(course=course, student=user, status="Pending")
    
    # เปลี่ยนเส้นทางไปยังหน้าแดชบอร์ด
    return redirect('student_dashboard')

@login_required
def cancel_request(request, quota_id):
    quota_request = get_object_or_404(QuotaRequest, id=quota_id, student=request.user)

    # ตรวจสอบว่าคำร้องขอโควต้าอยู่ในสถานะที่สามารถยกเลิกได้
    if quota_request.status in ['Complete', 'Pending']:
        course = quota_request.course
        quota_request.status = 'cancelled'
        quota_request.save()
        
        # คืนจำนวนที่นั่งในหลักสูตร
        course.available_seats += 1
        course.save()
        
        messages.success(request, "Your quota request has been cancelled and the seat has been refunded.")
    else:
        messages.error(request, "This quota request cannot be cancelled.")

    return redirect('student_dashboard')

@login_required
def add_course(request):
    if request.method == "POST":
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('student_dashboard')
    else:
        form = CourseForm()
    return render(request, 'students/add_course.html', {'form': form})

@login_required
def enroll_course(request, course_id):
    if request.method == 'POST':
        course = get_object_or_404(Course, id=course_id)
        
        # ตรวจสอบว่าผู้ใช้ได้ลงทะเบียนในหลักสูตรนี้แล้วหรือไม่
        existing_request = QuotaRequest.objects.filter(course=course, student=request.user).first()

        if existing_request:
            # ถ้าผู้ใช้ได้ลงทะเบียนแล้ว ให้แสดงข้อความแจ้งเตือน
            messages.warning(request, 'You have already enrolled in this course.')
            return redirect('student_dashboard')
        else:
            # ถ้ายังไม่ลงทะเบียนให้สร้างคำขอควอทาใหม่
            QuotaRequest.objects.create(student=request.user, course=course, status="Complete")
            # ลดจำนวนที่นั่งว่าง
            course.available_seats -= 1
            course.save()
            return redirect('student_dashboard')

    return redirect('student_dashboard')