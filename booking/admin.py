from datetime import datetime,timedelta
import re
from django.contrib import admin
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.urls import path
from django import forms
from django.contrib import messages
from django.shortcuts import render
from django.utils import timezone

from django.conf import settings

import csv
from .models import PopulateAppError,Appointment,Staff,Service,Client
from appointment.models import StaffMember,WorkingHours,AppointmentRequest
from appointment.models import Service as AppService
from appointment.models import Appointment as AppAppointment

class StaffAdmin(admin.ModelAdmin):
    list_display = ['first_name','last_name','team_member_id','phone_number','email','status','job_title',]
    search_fields = ('first_name','last_name','mobile_number','email',)

    # Define a custom admin action
    actions = ['import_staff_from_csv','process_selected_staff']

    # Define custom admin view to upload CSV
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('import-csv/', self.import_csv_view, name='import_staff_csv'),
        ]
        return custom_urls + urls

    def process_selected_staff(self, request, queryset):
        # Iterate through the selected queryset
        for staff in queryset:
            staff.populate_app()

        self.message_user(request, "Selected staff members have been processed.")
    process_selected_staff.short_description = "Process selected staff members"    
    
    # Custom action to trigger CSV upload page (optional)
    def import_staff_from_csv(self, request, queryset):
        return HttpResponseRedirect('/admin/booking/staff/import-csv/')


    def import_csv_view(self, request):
        if request.method == "POST" and request.FILES.get('csv_file'):
            try:
                # Call the model's import method
                Staff.import_from_csv(request.FILES['csv_file'])
                messages.success(request, "CSV file uploaded and staff members created/updated successfully.")
            except Exception as e:
                messages.error(request, f"Error importing CSV: {str(e)}")
            return HttpResponseRedirect("../")  # Redirect back to the appointment list

        return render(request, 'admin/import_csv.html', {})

admin.site.register(Staff, StaffAdmin)

class ClientAdmin(admin.ModelAdmin):
    list_display = ['full_name','client_id','mobile_number','email','added']
    search_fields = ('full_name','mobile_number','email',)

    # Define a custom admin action
    actions = ['import_client_from_csv','process_selected_clients']

    # Define custom admin view to upload CSV
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('import-csv/', self.import_csv_view, name='import_client_csv'),
        ]
        return custom_urls + urls

    def process_selected_clients(self, request, queryset):
        # Iterate through the selected queryset
        for client in queryset:
            client.populate_app()
        self.message_user(request, "Selected clients have been processed.")
    
    process_selected_clients.short_description = "Process selected clients"    
    
    # Custom action to trigger CSV upload page (optional)
    def import_client_from_csv(self, request, queryset):
        return HttpResponseRedirect('/admin/booking/client/import-csv/')


    def import_csv_view(self, request):
        if request.method == "POST" and request.FILES.get('csv_file'):
            try:
                # Call the model's import method
                Client.import_from_csv(request.FILES['csv_file'])
                messages.success(request, "CSV file uploaded and Clients created/updated successfully.")
            except Exception as e:
                messages.error(request, f"Error importing CSV: {str(e)}")
            return HttpResponseRedirect("../")  # Redirect back to the appointment list

        return render(request, 'admin/import_csv.html', {})

admin.site.register(Client, ClientAdmin)


class ServiceAdmin(admin.ModelAdmin):
    list_display = ['service_id','name','price','category_name','treatment_type',]
    search_fields = ('service_id','name','category_name',)

    # Define a custom admin action
    actions = ['import_service_from_csv','process_selected_service']

    # Define custom admin view to upload CSV
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('import-csv/', self.import_csv_view, name='import_service_csv'),
        ]
        return custom_urls + urls

    def process_selected_service(self, request, queryset):
        # Iterate through the selected queryset
        for service in queryset:
            service.populate_app()
        self.message_user(request, "Selected services have been processed.")

    process_selected_service.short_description = "Process selected services"    
    
    
    # Custom action to trigger CSV upload page (optional)
    def import_staff_from_csv(self, request, queryset):
        return HttpResponseRedirect('/admin/booking/service/import-csv/')


    def import_csv_view(self, request):
        if request.method == "POST" and request.FILES.get('csv_file'):
            try:
                # Call the model's import method
                Service.import_from_csv(request.FILES['csv_file'])
                messages.success(request, "CSV file uploaded and staff members created/updated successfully.")
            except Exception as e:
                messages.error(request, f"Error importing CSV: {str(e)}")
            return HttpResponseRedirect("../")  # Redirect back to the appointment list

        return render(request, 'admin/import_csv.html', {})

admin.site.register(Service, ServiceAdmin)

class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['ref','client','team_member','status','created_dt','scheduled_date','service','duration','price','deposit_paid']
    search_fields = ('ref','client','team_member','service',)

    # Define a custom admin action
    actions = ['import_appointments_from_csv','process_selected_appointment']

    # Define custom admin view to upload CSV
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('import-csv/', self.import_csv_view, name='import_appointments_csv'),
        ]
        return custom_urls + urls

    # Custom view to handle CSV file upload
    def process_selected_appointment(self, request, queryset):
        # Iterate through the selected queryset
        try:
            for appointment in queryset:
                appointment.populate_app()
            self.message_user(request, "Selected appointments have been processed.")
    
        except PopulateAppError as e:
            messages.error(request, e)

    process_selected_appointment.short_description = "Process selected appointments"    
    
    # Custom action to trigger CSV upload page (optional)
    def import_appointments_from_csv(self, request, queryset):
        return HttpResponseRedirect('/admin/booking/appointment/import-csv/')


    def import_csv_view(self, request):
        if request.method == "POST" and request.FILES.get('csv_file'):
            try:
                # Call the model's import method
                Appointment.import_from_csv(request.FILES['csv_file'])
                messages.success(request, "CSV file uploaded and appointments created/updated successfully.")
            except Exception as e:
                messages.error(request, f"Error importing CSV: {str(e)}")
            return HttpResponseRedirect("../")  # Redirect back to the appointment list

        return render(request, 'admin/import_csv.html', {})

# Register the custom AppointmentAdmin
admin.site.register(Appointment, AppointmentAdmin)
