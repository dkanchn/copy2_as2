from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required


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

class CustomLoginView(LoginView):
    template_name = 'login.html'  # ใช้ template สำหรับหน้า login

