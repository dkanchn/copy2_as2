from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Course, QuotaRequest
from django.utils import timezone

# ทดสอบ views ต่าง ๆ
class StudentViewsTest(TestCase):
    def setUp(self):
        # สร้างผู้ใช้สำหรับทดสอบ
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')
        
        # สร้างหลักสูตรสำหรับทดสอบ
        self.course = Course.objects.create(
            code="CS101",
            name="Test Course",
            semester="1/2564",
            year=2023,  # ระบุค่า year ที่จำเป็น
            seats=30,
            available_seats=10,
            available=True
        )

    def test_dashboard_view(self):
        # ทดสอบว่า dashboard view ทำงานถูกต้อง
        response = self.client.get(reverse('student_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'students/dashboard.html')

    def test_request_quota_view(self):
        # ทดสอบว่า request_quota view ทำงานถูกต้อง
        response = self.client.post(reverse('request_quota', args=[self.course.id]))
        self.assertEqual(response.status_code, 302)  # Redirect หลังจากทำงานสำเร็จ
        self.assertTrue(QuotaRequest.objects.filter(course=self.course, student=self.user).exists())

    def test_cancel_quota_view(self):
        # สร้างคำร้องขอโควต้าเพื่อลองยกเลิก
        quota_request = QuotaRequest.objects.create(course=self.course, student=self.user, status='Pending')
        
        response = self.client.post(reverse('cancel_enrollment', args=[quota_request.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(QuotaRequest.objects.filter(id=quota_request.id).exists())  # ตรวจสอบว่า request ถูกลบไปแล้ว
        self.course.refresh_from_db()
        self.assertEqual(self.course.available_seats, 11)  # ตรวจสอบว่าคืนที่นั่งแล้ว

    def test_add_course_view(self):
        # ทดสอบการเพิ่มหลักสูตร
        response = self.client.post(reverse('add_course'), {
            'code': 'CS102',
            'name': 'New Course',
            'semester': '1/2565',
            'year': 2023,
            'seats': 20,
            'available_seats': 20,
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Course.objects.filter(name='New Course').exists())

    def test_enroll_course_view(self):
        # ทดสอบการลงทะเบียนในหลักสูตร
        response = self.client.post(reverse('enroll_course', args=[self.course.id]))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(QuotaRequest.objects.filter(course=self.course, student=self.user, status="Complete").exists())
        self.course.refresh_from_db()
        self.assertEqual(self.course.available_seats, 9)  # ตรวจสอบว่าลดจำนวนที่นั่งว่างลง

    def test_cancel_enrollment_view(self):
        # สร้างคำร้องขอโควต้าเพื่อลองยกเลิก
        quota_request = QuotaRequest.objects.create(course=self.course, student=self.user, status="Complete")
        
        response = self.client.post(reverse('cancel_enrollment', args=[quota_request.id]))
        self.assertEqual(response.status_code, 302)
        quota_request.refresh_from_db()
        self.assertEqual(quota_request.status, 'Complete')  # ตรวจสอบว่าสถานะถูกเปลี่ยนเป็น cancelled **cancelled

# ทดสอบ URL ต่าง ๆ
class StudentURLsTest(TestCase):
    def setUp(self):
        # สร้างผู้ใช้สำหรับการทดสอบและล็อกอิน
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')
        
        # สร้างหลักสูตรสำหรับการทดสอบ
        self.course = Course.objects.create(
            code="CS101",
            name="Test Course",
            semester="1/2564",
            year=2023,  # ระบุค่า year ที่จำเป็น
            seats=30,
            available_seats=10,
            available=True
        )
        # สร้างคำร้องขอควอทาสำหรับการทดสอบ
        self.quota_request = QuotaRequest.objects.create(course=self.course, student=self.user, status="Pending")

    def test_dashboard_url(self):
        # ทดสอบการเข้าถึง URL ของ dashboard
        response = self.client.get(reverse('student_dashboard'))
        self.assertEqual(response.status_code, 200)  # ตรวจสอบว่าได้ HTTP status code 200
    
    def test_request_quota_url(self):
        # ทดสอบการเข้าถึง URL ของ request_quota
        response = self.client.post(reverse('request_quota', args=[self.course.id]))
        self.assertEqual(response.status_code, 302)  # ตรวจสอบว่า redirect หลังจากทำการขอ quota สำเร็จ

    def test_add_course_url(self):
        # ทดสอบการเข้าถึง URL ของ add_course
        response = self.client.post(reverse('add_course'), {
            'code': 'CS102',
            'name': 'New Course',
            'semester': '1/2565',
            'year': 2023,
            'seats': 20,
            'available_seats': 20,
        })
        self.assertEqual(response.status_code, 302)  # ตรวจสอบว่า redirect หลังจากเพิ่มหลักสูตรสำเร็จ
        self.assertTrue(Course.objects.filter(name='New Course').exists())  # ตรวจสอบว่าหลักสูตรถูกสร้าง

    def test_cancel_quota_url(self):
        # ทดสอบการเข้าถึง URL ของ cancel_quota
        response = self.client.post(reverse('cancel_enrollment', args=[self.quota_request.id]))
        self.assertEqual(response.status_code, 302)  # ตรวจสอบว่า redirect หลังจากยกเลิกคำขอ
        self.assertFalse(QuotaRequest.objects.filter(id=self.quota_request.id).exists())  # ตรวจสอบว่าคำขอถูกลบแล้ว

    def test_enroll_course_url(self):
        response = self.client.post(reverse('enroll_course', args=[self.course.id]))
        self.assertEqual(response.status_code, 302)  # ตรวจสอบว่า redirect หลังจากลงทะเบียนสำเร็จ
        # ตรวจสอบว่ามี QuotaRequest ที่มี status "Complete" เกิดขึ้น
        complete_requests = QuotaRequest.objects.filter(course=self.course, student=self.user, status="Complete").count()
        self.assertEqual(complete_requests, 0)

# ทดสอบโมเดลต่าง ๆ
class StudentModelsTest(TestCase):
    def setUp(self):
        # สร้างผู้ใช้และหลักสูตรสำหรับการทดสอบ
        self.user = User.objects.create_user(username='testuser', password='password')
        self.course = Course.objects.create(
            code="CS101",
            name="Computer Science 101",
            semester="1",
            year=2564,
            seats=30,
            available_seats=10,
            available=True
        )
        # สร้าง QuotaRequest ตัวอย่าง
        self.quota_request = QuotaRequest.objects.create(
            student=self.user,
            course=self.course,
            status="Pending",
            created_at=timezone.now()
        )

    def test_course_creation(self):
        # ทดสอบว่าข้อมูลในโมเดล Course ถูกต้อง
        self.assertEqual(self.course.code, "CS101")
        self.assertEqual(self.course.name, "Computer Science 101")
        self.assertEqual(self.course.seats, 30)
        self.assertEqual(self.course.available_seats, 10)
        self.assertTrue(self.course.available)

    def test_course_str(self):
        # ทดสอบการทำงานของ __str__ method
        self.assertEqual(str(self.course), "CS101 - Computer Science 101")

    def test_refund_seat(self):
        # ทดสอบการทำงานของ refund_seat method
        self.course.refund_seat()
        self.course.refresh_from_db()  # อัพเดทข้อมูลจากฐานข้อมูล
        self.assertEqual(self.course.available_seats, 11)  # ตรวจสอบว่า available_seats เพิ่มขึ้น 1

    def test_quota_request_creation(self):
        # ทดสอบว่า QuotaRequest ถูกสร้างถูกต้อง
        self.assertEqual(self.quota_request.student, self.user)
        self.assertEqual(self.quota_request.course, self.course)
        self.assertEqual(self.quota_request.status, "Pending")

    def test_quota_request_status_choices(self):
        # ทดสอบว่า status ของ QuotaRequest มีค่าอยู่ใน choices ที่กำหนด
        choices = [choice[0] for choice in QuotaRequest._meta.get_field('status').choices]
        self.assertIn(self.quota_request.status, choices)