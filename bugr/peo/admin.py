from .models import Lab
from django.contrib import admin
from django import forms
from osm_field.widgets import OSMWidget


class LabAdminForm(forms.ModelForm):
    class Meta:
        model = Lab
        widgets = {
            'location': OSMWidget('location_lat', 'location_lon'),
        }
        fields = '__all__'


@admin.register(Lab)
class LabAdmin(admin.ModelAdmin):
    form = LabAdminForm
