from .models import Lab
from django.contrib import admin


@admin.register(Lab)
class LabAdmin(admin.ModelAdmin):
    pass