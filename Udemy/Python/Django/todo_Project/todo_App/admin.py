from django.contrib import admin
from .models import Todo

class TodoAdmin(admin.ModelAdmin):
    readonly_fields = ('create_date', ) # Для отображения даты создания записи в панели администратора

admin.site.register(Todo, TodoAdmin)
