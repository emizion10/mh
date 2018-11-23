from django.shortcuts import render
from django.shortcuts import redirect,get_object_or_404,reverse
from django.views.generic import ListView,CreateView,DetailView,UpdateView,DeleteView
from mainapp.models import Hostel,Notifications,Warden,Student,Fees
from mainapp.forms import NotificationsForm,StudentForm,FeesForm
from django.contrib.auth.models import User
from datetime import datetime
from django.urls import reverse_lazy


# Create your views here.

class HostelList(ListView):
    context_object_name='hostel_list'
    model= Hostel
    template_name= 'mainapp/admin.html'


#
# def admin_page(request):
#     return render(request,'mainapp/admin.html',{})

def profile(request):
    fee_list= Fees.objects.filter(sid=request.user.student)

    return render(request,'mainapp/profile.html',{'fee_list':fee_list,})


# def admin_login(request):
#     return render(request,'mainapp/card.html',{})

class NotificationList(ListView):
    context_object_name='notification_list'
    model=Notifications
    def get_queryset(self):
        return Notifications.objects.order_by('-publish_time')
    template_name= 'mainapp/index.html'


class NotificationCreate(CreateView):
    model=Notifications

    def get_success_url(self):
        return reverse('mainapp:admin_page')
    form_class = NotificationsForm
    template_name = 'mainapp/new_notification.html'


class CreateStudent(CreateView):
    model=User

    def get_success_url(self):
        return reverse('mainapp:index')
    form_class = StudentForm
    def form_valid(self, form):
        c = {'form': form, }
        usr = form.save(commit=False)
        # Cleaned(normalized) data
        name = form.cleaned_data['name']
        address = form.cleaned_data['address']
        Class = form.cleaned_data['Class']
        dept = form.cleaned_data['dept']
        dob = form.cleaned_data['dob']
        phno = form.cleaned_data['phno']
        password = form.cleaned_data['password']
        propic = form.cleaned_data['propic']

        wl = get_object_or_404(Warden,warden_name=self.request.user)
        hname = str(wl.hostel)
        hostel_lis = Hostel.objects.get(hostel_name=hname)
        usr.set_password(password)
        usr.save()

        # Create UserProfile model
        Student.objects.create(std_username=usr, name=name,propic=propic,address=address,Class=Class,dept=dept,dob=dob,phno=phno,hostel=hostel_lis)

        return super(CreateStudent, self).form_valid(form)

    template_name = 'mainapp/newstudent.html'

class AddFees(CreateView):
    model=Fees

    def get_success_url(self):
        return reverse('mainapp:student_list')
    form_class = FeesForm
    template_name = 'mainapp/add_fees.html'

    def form_valid(self, form):
        c = {'form': form, }
        mess_fee = form.cleaned_data['mess_fee']
        hostel_fee = form.cleaned_data['hostel_fee']

        month = form.cleaned_data['month']
        # sid = form.cleaned_data['sid']

        # student = self.kwargs.get("pk")
        st = get_object_or_404(Student,pk=self.kwargs['pk'])
        # form.instance.student = self.student
        Fees.objects.create(sid=st,mess_fee=mess_fee,hostel_fee=hostel_fee,month=month)
        return super(AddFees,self).form_valid(form)



class StudentList(ListView):
    context_object_name='student_list'
    model=Student
    def get_queryset(self):
        user=self.request.user

        hostel_l =  Warden.objects.filter(warden_name=user).values_list('hostel',flat=True)
        return Student.objects.filter(hostel__in=hostel_l)

    template_name= 'mainapp/studentlist.html'



class HostelWiseStudentList(ListView):
     context_object_name='student_list'
     model=Student
     def get_queryset(self):
        host = get_object_or_404(Hostel,pk=self.kwargs['pk'])
        return Student.objects.filter(hostel=host)
     template_name= 'mainapp/hostel_wise_list.html'



class StudentProfile(DetailView):
    context_object_name='student'
    model = Student
    template_name= 'mainapp/student_profile.html'


    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(StudentProfile, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['fee_list'] = Fees.objects.filter(sid=self.object)
        return context


class PayFee(DetailView):
    model = Fees
    context_object_name='fee_detail'
    def get_object(self):
       fee_paid = get_object_or_404(Fees,pk=self.kwargs['pk'])
       # fee_paid.pay_date = datetime.date.today()
       # fee_paid.save()
       fee_paid.pay()
       return fee_paid
       # return Fees.objects.filter(pk=self.kwargs['pk'])
    template_name= 'mainapp/invoice.html'


class ManageNotifications(ListView):
     context_object_name='notify_list'
     model=Notifications
     def get_queryset(self):
        note =  Warden.objects.get(warden_name=self.request.user)

        return Notifications.objects.filter(author=note).order_by('-publish_time')

     template_name= 'mainapp/manage_notifications.html'

class UpdateNotifications(UpdateView):
    model = Notifications
    fields = ['title','msg']
    template_name= 'mainapp/update_notification.html'

    def get_success_url(self):
        return reverse('mainapp:manage_notification')

class DeleteNotifications(DeleteView):
    model = Notifications
    success_url = reverse_lazy('mainapp:manage_notification')
