from django.contrib import admin
from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', 'phone', 'document_info', 'dormitory_needed')
    search_fields = ('user__last_name', 'user__first_name', 'middle_name', 'phone')
    list_filter = ('doc_type', 'dormitory_needed')
