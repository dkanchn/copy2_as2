from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from students.models import Course, QuotaRequest

# Create your tests here.
class UserLoginViewTest(TestCase):

    def setUp(self):
        # สร้าง user สำหรับการทดสอบการเข้าสู่ระบบ
        self.user = User.objects.create_user(username='testuser', password='12345')

    def test_login_view(self):
        # ทดสอบการเข้าสู่ระบบ
        login = self.client.login(username='testuser', password='12345')
        self.assertTrue(login)

        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/login.html')

class UserLoginViewTest(TestCase):
    def setUp(self):
        # สร้างผู้ใช้ปกติและผู้ดูแลระบบสำหรับการทดสอบ
        self.student_user = User.objects.create_user(username='student', password='password')
        self.staff_user = User.objects.create_user(username='staff', password='password', is_staff=True)

    def test_login_student_redirect_dashboard(self):
        # ทดสอบการเข้าสู่ระบบของนักเรียนและเปลี่ยนเส้นทางไปยัง student_dashboard
        response = self.client.post(reverse('login'), {'username': 'student', 'password': 'password'})
        self.assertRedirects(response, reverse('student_dashboard'))

    def test_login_staff_redirect_admin(self):
        # ทดสอบการเข้าสู่ระบบของผู้ดูแลระบบและเปลี่ยนเส้นทางไปยังหน้า admin
        response = self.client.post(reverse('login'), {'username': 'staff', 'password': 'password'})
        self.assertRedirects(response, reverse('admin:index'))

    def test_login_invalid_credentials(self):
        # ทดสอบการเข้าสู่ระบบด้วยข้อมูลไม่ถูกต้อง
        response = self.client.post(reverse('login'), {'username': 'invalid', 'password': 'wrong'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/login.html')

class ApproveQuotaRequestsViewTest(TestCase):
    def setUp(self):
        # สร้างผู้ใช้ผู้ดูแลระบบและลงชื่อเข้าใช้
        self.staff_user = User.objects.create_user(username='staff', password='password', is_staff=True)
        self.client.login(username='staff', password='password')
        # สร้าง Course ก่อน
        #self.course = Course.objects.create(name="Course Name", year=2024)
        self.course = Course.objects.create(name="Course Name", year=2024, available_seats=10)

        # สร้าง QuotaRequest ที่มีสถานะเป็น "Pending"
        self.quota_request = QuotaRequest.objects.create(student=self.staff_user, course_id=1, status="Pending")

    def test_approve_quota_requests_view_loads(self):
        # ทดสอบว่าหน้า approve_quota_requests โหลดได้
        response = self.client.get(reverse('approve_quota_requests'))
        self.assertEqual(response.status_code, 200)
        #self.assertTemplateUsed(response, 'admin/approve_quota_requests.html')

    def test_approve_quota_request(self):
        # ทดสอบการอนุมัติ QuotaRequest
        response = self.client.post(reverse('approve_quota_requests'), {'quota_id': self.quota_request.id})
        self.quota_request.refresh_from_db()
        self.assertEqual(self.quota_request.status, "Approved")
        self.assertRedirects(response, reverse('approve_quota_requests'))

class ManageQuotaRequestsViewTest(TestCase):
    def setUp(self):
        # สร้าง Course ก่อน
        self.course = Course.objects.create(name="Sample Course", year=2024, available_seats=10)
        
        # สร้างผู้ใช้ผู้ดูแลระบบและ QuotaRequest สำหรับการทดสอบ
        self.staff_user = User.objects.create_user(username='staff', password='password', is_staff=True)
        self.client.login(username='staff', password='password')
        self.quota_request = QuotaRequest.objects.create(student=self.staff_user, course_id=1, status="Pending")

    def test_manage_quota_requests_view_loads(self):
        # ทดสอบว่าหน้า manage_quota_requests โหลดได้
        response = self.client.get(reverse('manage_quota_requests'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin/manage_quota_requests.html')

    def test_approve_quota_request(self):
        # ทดสอบการเปลี่ยนสถานะเป็น "approved"
        response = self.client.post(reverse('manage_quota_requests'), {
            'quota_request_id': self.quota_request.id,
            'action': 'approve'
        })
        self.quota_request.refresh_from_db()
        self.assertEqual(self.quota_request.status, 'approved')

    def test_reject_quota_request(self):
        # ทดสอบการเปลี่ยนสถานะเป็น "rejected"
        response = self.client.post(reverse('manage_quota_requests'), {
            'quota_request_id': self.quota_request.id,
            'action': 'reject'
        })
        self.quota_request.refresh_from_db()
        self.assertEqual(self.quota_request.status, 'rejected')
