import csv
import re
from datetime import datetime,timedelta
from django.utils import timezone,dateparse
from django.db import IntegrityError
from django.db import models
from django.contrib.auth.models import User
from django.db.models import F, Value
from django.db.models.functions import Concat

from appointment.models import StaffMember,WorkingHours
from appointment.models import Service as AppService
from appointment.models import Appointment as AppAppointment
from appointment.models import AppointmentRequest as AppAppointmentRequest


class PopulateAppError(Exception):
    pass

# Create your models here.
class Staff(models.Model):
    #First Name	
    #Last Name	
    #Phone Number	
    #Email	
    #Status	
    #Birthday	
    #Country	
    #Job Title	
    #Start Date	
    #End Date	
    #Employment Type	
    #Team Member Id	
    #Notes	
    #Appointments	
    #User Permission	
    #Address	
    #Emergency Contact	
    #Service Commission	
    #Product Commission	
    #Voucher Commission
    first_name	        = models.CharField(max_length=255,)
    last_name	        = models.CharField(max_length=255,)
    phone_number	    = models.CharField(max_length=255,)
    email	            = models.CharField(max_length=255,)
    status	            = models.CharField(max_length=20,)
    birthday	        = models.DateField(blank=True, null=True)
    country	            = models.CharField(max_length=255,blank=True, null=True)
    job_title	        = models.CharField(max_length=255,blank=True, null=True)
    start_date	        = models.DateField(blank=True, null=True)
    end_date	        = models.DateField(blank=True, null=True)
    employment_type	    = models.CharField(max_length=20,blank=True, null=True)
    team_member_id	    = models.CharField(max_length=20,blank=True, null=True)
    notes	            = models.TextField(blank=True, null=True)
    appointments	    = models.CharField(max_length=20,blank=True, null=True)
    user_permission	    = models.CharField(max_length=20,blank=True, null=True)
    address	            = models.CharField(max_length=255,blank=True, null=True)
    emergency_contact	= models.CharField(max_length=255,blank=True, null=True)
    service_commission	= models.CharField(max_length=255,blank=True, null=True)
    product_commission	= models.CharField(max_length=255,blank=True, null=True)
    voucher_commission  = models.CharField(max_length=255,blank=True, null=True)
    cdt = models.DateTimeField(auto_now_add=True, null=True)
    udt = models.DateTimeField(auto_now=True, null=True)

    def populate_app(self):
        print('populate_app',self.first_name,self.team_member_id)
        if not self.team_member_id:
            print('user not found, creating')
            user = User.objects.create_user(self.email, self.email, '')
            user.first_name = self.first_name
            user.last_name = self.last_name
            user.is_staff = True
            user.save()
            self.team_member_id = user.id
            self.save()
            staffmember = StaffMember(user=user,slot_duration=30,work_on_saturday=True,work_on_sunday=True,lead_time='09:00',finish_time='20:00')
            staffmember.save()
            for week in range(0,7):
                wh = WorkingHours(staff_member=staffmember,day_of_week=week,start_time='09:00',end_time='20:00')
                wh.save()
        else:
            print(f'team_member_id:{self.team_member_id}')
            user = User.objects.get(id=int(self.team_member_id))
            print('user found')
            user.first_name = self.first_name
            user.last_name = self.last_name
            user.email = self.email
            user.is_staff = True
            user.save()
            try:
                staffmember = StaffMember.objects.get(user=user)
                print('staffmember found')
            except StaffMember.DoesNotExist:
                print('staffmember not found, creating')
                staffmember = StaffMember(user=user,slot_duration=30,work_on_saturday=True,work_on_sunday=True,lead_time='09:00',finish_time='20:00')
                staffmember.save()

            whs = WorkingHours.objects.filter(staff_member=staffmember)
            print('whs len:'+str(len(whs)))
            if not len(whs):
                print('WorkingHours not found, creating')
                for week in range(0,7):
                    wh = WorkingHours(staff_member=staffmember,day_of_week=week,start_time='09:00',end_time='20:00')
                    wh.save()


    @classmethod
    def import_from_csv(cls, csv_file):
        reader = csv.DictReader(csv_file.read().decode('utf-8').splitlines())
        for row in reader:
            try:
                print (row)
                if row['First Name'] or row['Last Name']:
                    staff_data = {
                        'first_name'	    : row['First Name'],	
                        'last_name'	        : row['Last Name'],	
                        'phone_number'	    : row['Phone Number'],	
                        'email'	            : row['Email'],	
                        'status'	        : row['Status'],	
                        'birthday'	        : dateparse.parse_date(row['Birthday']),
                        'country'	        : row['Country'],	
                        'job_title'	        : row['Job Title'],	
                        'start_date'	    : dateparse.parse_date(row['Start Date']),	
                        'end_date'	        : dateparse.parse_date(row['End Date']),	
                        'employment_type'	: row['Employment Type'],	
                        'team_member_id'    : row['Team Member Id'],	
                        'notes'	            : row['Notes'],	
                        'appointments'	    : row['Appointments'],	
                        'user_permission'	: row['User Permission'],	
                        'address'	        : row['Address'],	
                        'emergency_contact'	: row['Emergency Contact'],
                        'service_commission':row['Service Commission'],	
                        'product_commission':row['Product Commission'],	
                        'voucher_commission': row['Voucher Commission'],
                    }

                    staff, created = cls.objects.update_or_create(first_name=row['First Name'],last_name=row['Last Name'], defaults=staff_data)

            except IntegrityError as e:
                print(f"Error importing appointment {row['First Name']} {row['Last Name']}: {e}")
            except Exception as e:
                print(f"Error processing row {row['First Name']} {row['Last Name']}: {e}")

class Client(models.Model):
    #Client ID	First Name	Last Name	Full Name	Blocked	Block Reason	Appointments	No-shows	Total Sales	Outstanding	Gender	Mobile Number	Telephone	Email	Accepts Marketing	Accepts SMS Marketing	Address	Apartement Suite	Area	City	State	Post Code	Date of Birth	Added	Note	Referral Source
    client_id       = models.CharField(max_length=20, unique=True,default=0)	
    first_name	    = models.CharField(max_length=255,blank=True,null=True)
    last_name	    = models.CharField(max_length=255,blank=True,null=True)
    full_name	    = models.CharField(max_length=255,)
    blocked	        = models.CharField(max_length=20,blank=True,null=True)
    block_reason	= models.CharField(max_length=255,blank=True,null=True)
    appointments	= models.IntegerField(blank=True,null=True)
    no_shows	    = models.IntegerField(blank=True,null=True)
    total_sales	    = models.DecimalField(max_digits=6, decimal_places=2,blank=True,null=True)
    outstanding	    = models.DecimalField(max_digits=6, decimal_places=2,blank=True,null=True)
    gender	        = models.CharField(max_length=20,blank=True,null=True)
    mobile_number	= models.CharField(max_length=255,blank=True,null=True)
    telephone	    = models.CharField(max_length=255,blank=True,null=True)
    email	        = models.CharField(max_length=255,blank=True,null=True)
    accepts_marketing	    = models.CharField(max_length=20,blank=True,null=True)
    accepts_sms_marketing	= models.CharField(max_length=20,blank=True,null=True)
    address	        = models.CharField(max_length=255,blank=True,null=True)
    suite	        = models.CharField(max_length=255,blank=True,null=True)
    area	        = models.CharField(max_length=255,blank=True,null=True)
    city	        = models.CharField(max_length=255,blank=True,null=True)
    state	        = models.CharField(max_length=255,blank=True,null=True)
    post_code	    = models.CharField(max_length=20,blank=True,null=True)
    date_of_birth	= models.DateField(blank=True, null=True)
    added	        = models.DateField(blank=True, null=True)
    note	        = models.TextField(blank=True,null=True)
    referral_source = models.CharField(max_length=255,blank=True,null=True)
    user_id 	    = models.IntegerField(blank=True,null=True)

    def populate_app(self):
        print('populate_app',self.full_name)

        username = re.sub(r'[^a-zA-Z0-9@+\-_\u0400-\u04FF\u00C0-\u00FF]', '.', self.full_name)

        print(self.first_name,self.full_name,username,self.added)

        try:
            user = User.objects.get(username=username)
            print('user found')
        except User.DoesNotExist:
            print('user not found, creating')
            user = User.objects.create_user(username, self.email, '')
            user.first_name = self.first_name
            user.last_name = self.last_name
            user.email = self.email
            if self.added:
                combined_datetime = datetime.combine(self.added, datetime.min.time())
                user.date_joined = timezone.make_aware(combined_datetime, timezone.get_current_timezone())

            user.save()

        if not self.user_id and self.user_id!=user.id:
            #TODO - id/username discrepancy 

            self.user_id = user.id
            self.save()

    @classmethod
    def import_from_csv(cls, csv_file):
        reader = csv.DictReader(csv_file.read().decode('utf-8').splitlines())
        for row in reader:
            try:
                print (row)
                if row['Client ID']:
                    data = {
                        'client_id'             : row['Client ID'],	
                        'first_name'	        : row['First Name'],	
                        'last_name'	            : row['Last Name'],	
                        'full_name'	            : row['Full Name'],	
                        'blocked'	            : row['Blocked'],	
                        'block_reason'	        : row['Block Reason'],	
                        'appointments'	        : row['Appointments'],	
                        'no_shows'	            : row['No-shows'],	
                        'total_sales'	        : row['Total Sales'],	
                        'outstanding'	        : row['Outstanding'],	
                        'gender'	            : row['Gender'],	
                        'mobile_number'	        : row['Mobile Number'],	
                        'telephone'	            : row['Telephone'],	
                        'email'	                : row['Email'],	
                        'accepts_marketing'     : row['Accepts Marketing'],
                        'accepts_sms_marketing' : row['Accepts SMS Marketing'],
                        'address'	            : row['Address'],	
                        'suite'	                : row['Apartement Suite'],	
                        'area'	                : row['Area'],	
                        'city'	                : row['City'],	
                        'state'	                : row['State'],	
                        'post_code'	            : row['Post Code'],
                        'date_of_birth'	        : dateparse.parse_date(row['Date of Birth']),	
                        'added'	                : dateparse.parse_date(row['Added']),	
                        'note'	                : row['Note'],	
                        'referral_source'       : row['Referral Source'],
                    }
                    
                    client, created = cls.objects.update_or_create(client_id=row['Client ID'], defaults=data)
                    if not created: break

            except IntegrityError as e:
                print(f"Error importing appointment {row['Client ID']} {row['Full Name']}: {e}")
            except Exception as e:
                print(f"Error processing row {row['Client ID']} {row['Full Name']}: {e}")



class Service(models.Model):
    #Service Name #Retail Price #Duration #Extra Time #Tax #Description #Category Name #Treatment Type #Resource #Online Booking #Available For #Voucher Sales #Commissions #Service ID #SKU
    service_id      = models.CharField(max_length=20,)
    name            = models.CharField(max_length=255,unique=True)
    price           = models.DecimalField(max_digits=6, decimal_places=2,)
    duration        = models.IntegerField()
    extra_time      = models.CharField(max_length=255,blank=True, null=True)
    tax             = models.CharField(max_length=255,blank=True, null=True)
    description     = models.TextField(blank=True, null=True)
    category_name   = models.CharField(max_length=255,)
    treatment_type  = models.CharField(max_length=255,blank=True, null=True)
    resource        = models.CharField(max_length=20,blank=True, null=True)
    online_booking  = models.CharField(max_length=20,blank=True, null=True)
    available_for   = models.CharField(max_length=20,blank=True, null=True)
    voucher_sales   = models.CharField(max_length=20,blank=True, null=True)
    commissions     = models.CharField(max_length=20,blank=True, null=True)
    sku             = models.CharField(max_length=20,blank=True, null=True)
    cdt = models.DateTimeField(auto_now_add=True, null=True)
    udt = models.DateTimeField(auto_now=True, null=True)

    def populate_app(self):
        print('populate_app',self.name)
        print(self.name,)

        try:
            srv = AppService.objects.get(name=self.name)
            print('AppService found, updating')
        except AppService.DoesNotExist:
            print('AppService not found, creating')
            srv = AppService(name=self.name)

        srv.category_name = self.category_name
        srv.description = self.description
        srv.duration = timedelta(minutes=self.duration)
        srv.price = self.price
        srv.currency = 'GBP'

        srv.save()


    @classmethod
    def sanitize_name(cls, name):
        name = re.sub('\s*-\s*From$','',name)
        name = re.sub(r'\(\s+', '(', name)
        name = re.sub(r'\s+\)', ')', name)
        name = re.sub(r'\s*,', ', ', name)
        name = re.sub(r'\s+', ' ', name).strip()
        return name

    @classmethod
    def import_from_csv(cls, csv_file):
        reader = csv.DictReader(csv_file.read().decode('utf-8').splitlines())
        for row in reader:
            try:
                name = cls.sanitize_name(row['Service Name'])
                print (row['Service Name'],name)
                if row['Service Name']:
                    data = {
                        'service_id'      : row['Service ID'], 
                        'name'            : name, 
                        'price'           : row['Retail Price'], 
                        'duration'        : parse_duration(row['Duration']), 
                        'extra_time'      : row['Extra Time'], 
                        'tax'             : row['Tax'], 
                        'description'     : row['Description'], 
                        'category_name'   : row['Category Name'],
                        'treatment_type'  : row['Treatment Type'], 
                        'resource'        : row['Resource'], 
                        'online_booking'  : row['Online Booking'], 
                        'available_for'   : row['Available For'], 
                        'voucher_sales'   : row['Voucher Sales'], 
                        'commissions'     : row['Commissions'], 
                        'sku'             : row['SKU'],
                    }
                    service, created = cls.objects.update_or_create(name=name, defaults=data)

            except IntegrityError as e:
                print(f"Error importing appointment {row['Service ID']} {row['Service Name']}: {e}")
            except Exception as e:
                print(f"Error processing row {row['Service ID']} {row['Service Name']}: {e}")


class Appointment(models.Model):
    #Ref #	Channel	Created Date	Created By	Client	Service	Scheduled Date	Time	Duration	Staff	Price	Status	Created on	Scheduled on

    ref = models.CharField(max_length=20, unique=True)
    client = models.CharField(max_length=255,)
    team_member = models.CharField(max_length=255,)
    status = models.CharField(max_length=20,)
    created_dt = models.DateTimeField()
    scheduled_date = models.DateField(null=True)
    scheduled_time = models.TimeField(null=True)
    service = models.CharField(max_length=255,)
    duration = models.IntegerField(null=True)
    created_by = models.CharField(max_length=255,null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    deposit_paid = models.DecimalField(max_digits=6, decimal_places=2,null=True,blank=True)
    channel = models.CharField(max_length=255,null=True)
    cdt = models.DateTimeField(auto_now_add=True, null=True)
    udt = models.DateTimeField(auto_now=True, null=True)

    def populate_app(self):
        print('populate_app',self.ref,self.status)
        print(self.ref,self.service,self.client,self.team_member,self.status)
        ref= 'F'+self.ref

        date1 = self.scheduled_date
        time1 = self.scheduled_time
        datetime1 = datetime.combine(date1, time1)
        datetime2 = datetime1 + timedelta(minutes=self.duration)
        time2 = datetime2.time()

        print(date1,time1,time2)
        svc = AppService.objects.filter(name__iexact=self.service)
        if len(svc)>0:
            print (svc[0])
        else:
            print(f'service {self.service} not found')
            raise PopulateAppError(f'service {self.service} not found')

        staff = Staff.objects.annotate(
                full_name=Concat(F('first_name'), Value(' '), F('last_name'))
            ).filter(full_name=self.team_member)
        if len(staff)>0:
            print (staff[0])
            user_id = staff[0].team_member_id
        else:
            print(f'staff member {self.team_member} not found')
            raise PopulateAppError(f'staff member {self.team_member} not found')
        

        try:
            client = Client.objects.get(full_name=self.client)
            print('client found')
        except Client.MultipleObjectsReturned:
            print('client found - multiple clients with the same name')
            client = Client.objects.filter(full_name=self.client)[0]

        except Client.DoesNotExist:
            print(f'client {self.client} not found')
            if self.client=='Walk-In':
                client = Client(full_name=self.client)
                client.save()
            else:
                raise PopulateAppError(f'client {self.client} not found')

        username = re.sub(r'[^a-zA-Z0-9@+\-_\u0400-\u04FF\u00C0-\u00FF]', '.', self.client)

        try:
            user = User.objects.get(username=username)
            print('user found')
        except User.DoesNotExist:
            print(f'client user {self.client} not found')
            client.populate_app()
            user = User.objects.get(id=client.user_id)

        try:
            appr = AppAppointmentRequest.objects.get(id_request=ref)
            print('AppointmentRequest found')
        except AppAppointmentRequest.DoesNotExist:
            appr = AppAppointmentRequest(id_request=ref)

            appr.date = date1
            appr.start_time = time1
            appr.end_time = time2
            appr.service = svc[0]
            appr.staff_member = StaffMember.objects.get(user_id=user_id)

            appr.save()

        try:
            app = AppAppointment.objects.get(id_request=ref)
            print('Appointment found')
        except AppAppointment.DoesNotExist:
            print('Appointment not found, creating')
            app = AppAppointment(id_request=ref)
#
            app.appointment_request = appr
            app.status = AppAppointment.Status.CANCELLED if self.status=='Canceled' or self.status=='Cancelled' else AppAppointment.Status.SCHEDULED
            app.amount_to_pay = self.price
            app.paid_deposit = self.deposit_paid
            app.client = user
            app.phone = client.mobile_number or client.telephone or '-none-'
            app.address = ", ".join(filter(None, [client.address,client.suite,client.area,client.city,client.state,client.post_code]))

            app.save()

    @classmethod
    def import_from_csv(cls, csv_file):
        reader = list(csv.DictReader(csv_file.read().decode('utf-8').splitlines()))

        print('import_from_csv')

        reading = None
        if reader[0].get('Ref #'):
            print('appointments')
            reading = 'a'
        elif reader[0].get('Payment Date'):
            print('payments')
            reading = 'p'

        for row in reader:
            if reading == 'a':
                try:
                    if row['Ref #']:
                        print (row)
                        #Ref #	Channel	Created Date	Created By	Client	Service	Scheduled Date	Time	Duration	Staff	Price	Status	Created on	Scheduled on
                        scheduled_on = parse_datetime(row['Scheduled on'])
                        print (scheduled_on)
                        print (scheduled_on.date())
                        appointment_data = {
                            'ref': row['Ref #'],
                            'channel': row['Channel'],
                            'client': row['Client'],
                            'team_member': row['Staff'],
                            'status': row['Status'],
                            'created_dt': parse_datetime(row['Created on']),
                            'scheduled_date': scheduled_on.date(),
                            'scheduled_time': scheduled_on.time(),
                            'service': Service.sanitize_name(row['Service']),
                            'duration': row['Duration'],
                            'created_by': row['Created By'],
                            'price': row['Price'],
                        }

                        # If an appointment with the same ref exists, update it; otherwise, create a new one
                        appointment, created = cls.objects.update_or_create(ref=row['Ref #'], defaults=appointment_data)
                except IntegrityError as e:
                    print(f"Error importing appointment {row['Ref #']}")
                    print(e)
                except Exception as e:
                    print(f"Error processing row {row['Ref #']}")
                    print(e)
            elif reading == 'p':
                try:
                    if row['Payment Date']:
                        print (row)
                        #"Payment Date","ID","Payment No.","Invoice Date","Invoice No.","Appointment Ref","Client","Client ID","Staff","Transaction","Method","Amount"
                        ref = '#' + row['Appointment Ref'].upper()
                        print(ref)
                        print(row['Transaction'])
                        if row['Transaction']=='Deposit':
                            try:
                                appointment = cls.objects.get(ref=ref)
                                appointment.deposit_paid = row['Amount']
                                print(f"Saving Appointment {ref}: {appointment.deposit_paid}")
                                appointment.save()
                            except cls.DoesNotExist:
                                print(f"Appointment {ref} does not exist")

                except Exception as e:
                    print(f"Error processing row {row['Payment Date']}")
                    print(e)

def parse_duration(duration_str):
    """
    Parse a duration string in the format '1h 45min' and convert it to minutes.
    """
    total_minutes = 0
    try:
        # Extract hours and minutes using regular expressions
        hours = 0
        minutes = 0
        parts = duration_str.split()
        for part in parts:
            if 'h' in part:
                hours = int(part.replace('h', '').strip())
            elif 'min' in part:
                minutes = int(part.replace('min', '').strip())

        # Convert hours to minutes and add the remaining minutes
        total_minutes = (hours * 60) + minutes
    except Exception as e:
        print(f"Error parsing duration string: {duration_str} - {e}")
    
    return total_minutes
    
def parse_datetime(datetime_str):
    """
    Parse a datetime string in the format "14 Dec 2024, 5:30pm" into a Python datetime object.
    """
    try:
        # Parse the naive datetime
        #naive_datetime = datetime.strptime(datetime_str, "%d %b %Y, %I:%M%p")
        naive_datetime = datetime.strptime(datetime_str, "%Y-%m-%d %I:%M %p")
        
        # Convert the naive datetime to an aware datetime (using the default timezone)
        aware_datetime = timezone.make_aware(naive_datetime, timezone.get_current_timezone())

        print(aware_datetime)
        return aware_datetime
    except ValueError:
        print(f"Error parsing datetime string: {datetime_str}")
        return None