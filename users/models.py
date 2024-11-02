from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # เชื่อมโยงกับ User
    student_id = models.CharField(max_length=10)  # รหัสนักเรียน

    def __str__(self):
        return self.user.username  # แสดงชื่อผู้ใช้