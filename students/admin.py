from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Course, QuotaRequest

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'semester', 'year', 'seats', 'available')

    def available(self, obj):
        return "Available" if obj.is_open else "Closed"
    available.short_description = 'Status'  # ชื่อคอลัมน์ในตาราง

@admin.register(QuotaRequest)
class QuotaRequestAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'status')
    list_filter = ('status',)
    search_fields = ('student__username', 'course__code')

