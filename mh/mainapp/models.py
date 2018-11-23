from django.db import models
from django.contrib.auth.models import User
# from datetime import datetime
import datetime
from django.utils import timezone


# Create your models here.
MONTH_CHOICES = (
    ("JAN", "January"),
    ("FEB", "February"),
    ("MAR", "March"),
    ("APR", "April"),
    ("MAY", "May"),
    ("JUN", "June"),
    ("JUL", "July"),
    ("AUG", "August"),
    ("SEP", "September"),
    ("OCT", "October"),
    ("NOV", "November"),
    ("DEC", "December"),
)

# DEPT_CHOICES = (
#     ("Computer Science","CSE"),
#     ("Mechanical Engineering","MECH"),
#     ("Civil Engineering","CIVIL"),
#     ("Electrical & Electronics","EEE"),
#     ("Electronics & Communication","ECE"),
#
# )

class Hostel(models.Model):
    hostel_name = models.CharField(max_length=30)
    capacity = models.PositiveIntegerField(blank=True, null=True)
    descrip = models.TextField(blank=True)
    hostelpic = models.ImageField(upload_to='hostels/',blank=True)

    def __str__(self):
        return self.hostel_name

class Warden(models.Model):
    warden_name = models.OneToOneField(User,on_delete=models.CASCADE)
    hostel = models.OneToOneField(Hostel,on_delete=models.CASCADE)

    def __str__(self):
        return str(self.warden_name)

class Student(models.Model):
    std_username = models.OneToOneField(User,on_delete=models.CASCADE)
    propic = models.ImageField(upload_to='images/',blank=True)
    name = models.CharField(blank=True, max_length=100)
    address = models.TextField(blank=True)
    Class = models.CharField(max_length=10,blank=False)
    dept = models.CharField(max_length=10, blank=False)
    dob = models.DateField(blank=False)
    phno = models.CharField(blank=True, max_length=20)
    hostel = models.ForeignKey(Hostel,on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Notifications(models.Model):
    author = models.ForeignKey(Warden,on_delete=models.CASCADE)
    title = models.CharField(blank=True, max_length=100)
    msg = models.TextField(blank=True)
    publish_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

class Fees(models.Model):
    sid = models.ForeignKey(Student,on_delete=models.CASCADE,null=True)
    mess_fee = models.PositiveIntegerField(null=False)
    hostel_fee = models.PositiveIntegerField(null=False)
    fee = models.PositiveIntegerField(null=True,blank=True)
    month = models.CharField(max_length=100,choices=MONTH_CHOICES)
    paid = models.BooleanField(default=False)
    enter_date = models.DateField(default=datetime.date.today)
    pay_date = models.DateField(blank=True,null=True)
    fine = models.PositiveIntegerField(blank=True,null=True)

    def __str__(self):
        return self.month

    def pay(self):
        self.pay_date = datetime.date.today()
        if (self.pay_date-self.enter_date).days>20 :
            self.fine = (self.pay_date-self.enter_date).days * 2
        else:
            self.fine = 0
        self.fee = self.mess_fee + self.hostel_fee + self.fine
        self.paid=True
        self.save()
