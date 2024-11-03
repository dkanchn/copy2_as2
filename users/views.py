from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.urls import reverse


# ฟังก์ชันสำหรับเข้าสู่ระบบ
def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            if user.is_staff:  # ตรวจสอบว่าผู้ใช้เป็นผู้ดูแลระบบหรือไม่
                return redirect('admin:index')  # นำทางไปยังหน้า admin
            else:
                return redirect('student_dashboard')  # นำทางไปยังหน้า dashboard สำหรับนักเรียน
        else:
            #messages.error(request, "Username หรือ Password ไม่ถูกต้อง")
            render(request, 'users/login.html')
    
    return render(request, 'users/login.html')

from django.contrib.auth.views import LoginView

#class CustomLoginView(LoginView):
#    template_name = 'login.html'  # ใช้ template สำหรับหน้า login
def custom_login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            if user.is_staff:  # ถ้าเป็นผู้ดูแลระบบ
                return redirect(reverse('admin:index'))
            else:  # ถ้าไม่ใช่ผู้ดูแลระบบ
                return redirect('student_dashboard')
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('login')  # กลับไปหน้า login ถ้าข้อมูลไม่ถูกต้อง

    return render(request, 'users/login.html')  # หน้า login template ของคุณ

# admin/views.py
from django.shortcuts import render, get_object_or_404, redirect
from students.models import QuotaRequest
from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def approve_quota_requests(request):
    quota_requests = QuotaRequest.objects.filter(status="Pending")
    
    if request.method == "POST":
        quota_id = request.POST.get("quota_id")
        quota_request = get_object_or_404(QuotaRequest, id=quota_id)
        quota_request.status = "Approved"
        quota_request.save()
        return redirect('approve_quota_requests')
    
    context = {
        'quota_requests': quota_requests,
    }
    return render(request, 'admin/manage_quota_requests.html', context)

@login_required
def manage_quota_requests(request):
    quota_requests = QuotaRequest.objects.filter(status='pending')

    if request.method == 'POST':
        quota_request_id = request.POST.get('quota_request_id')
        action = request.POST.get('action')
        quota_request = QuotaRequest.objects.get(id=quota_request_id)

        if action == 'approve':
            quota_request.status = 'approved'
        elif action == 'reject':
            quota_request.status = 'rejected'

        quota_request.save()

    return render(request, 'admin/manage_quota_requests.html', {'quota_requests': quota_requests})