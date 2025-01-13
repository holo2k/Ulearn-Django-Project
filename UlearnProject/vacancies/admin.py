from django.contrib import admin
from .models import PageElement


@admin.register(PageElement)
class PageElementAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'updated_at')
    search_fields = ('title',)
