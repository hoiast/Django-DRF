from django.contrib import admin
from employee_review.models import Employee, Review, Feedback


class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'created_at', 'updated_at']
    list_display_links = ['id', 'name']
    search_fields = ['name']


class ReviewAdmin(admin.ModelAdmin):
    list_display = ['id', 'employee', 'title',
                    'review', 'created_at', 'updated_at']
    list_display_links = ['id', 'employee', 'title', 'review']
    search_fields = ['employee', 'title', 'review']


class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['id', 'review', 'employee',
                    'pending', 'feedback', 'created_at', 'updated_at']
    list_display_links = ['id', 'review', 'employee', 'pending', 'feedback']
    search_fields = ['review', 'employee', 'pending', 'feedback']
    exclude = ['pending', 'feedback']


admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Feedback, FeedbackAdmin)
