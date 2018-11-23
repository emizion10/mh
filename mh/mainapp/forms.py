from django import forms
from mainapp.models import Notifications,Student,Hostel,Fees
from django.contrib.auth.models import User
from datetime import date
#
# DEPT_CHOICES = (
#     ("Computer Science","CSE"),
#     ("Mechanical Engineering","MECH"),
#     ("Civil Engineering","CIVIL"),
#     ("Electrical & Electronics","EEE"),
#     ("Electronics & Communication","ECE"),
#
# )

class NotificationsForm(forms.ModelForm):
    class Meta:
        model = Notifications
        fields = ('title','msg','author')

class StudentForm(forms.ModelForm):
      password = forms.CharField(widget=forms.PasswordInput)
      name = forms.CharField(max_length=100)
      propic = forms.ImageField(label='Select Image')
      address = forms.CharField()
      Class = forms.CharField(max_length=10)
      dept = forms.CharField(max_length=10)
      dob = forms.DateField()
      phno = forms.CharField(max_length=20)
      class Meta():
          model = User
          fields = ('username','password')

class FeesForm(forms.ModelForm):
    class Meta:
        model = Fees
        fields = ('mess_fee','hostel_fee','month')
