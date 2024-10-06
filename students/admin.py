from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Course, QuotaRequest

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'semester', 'year', 'seats', 'available_seats', 'available')

    def available(self, obj):
        return "Available" if obj.is_open else "Closed"
    available.short_description = 'Status'  # ชื่อคอลัมน์ในตาราง

@admin.register(QuotaRequest)
class QuotaRequestAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'status', 'created_at')
    actions = ['approve_requests']

    def approve_requests(self, request, queryset):
        queryset.update(status='Approved')

    approve_requests.short_description = "Approve selected quota requests"