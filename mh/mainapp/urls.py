from django.urls import path
from mainapp import views
from mainapp.views import NotificationList,CreateStudent,StudentList,StudentProfile,NotificationCreate,AddFees,HostelList,HostelWiseStudentList,PayFee,ManageNotifications
from mainapp.views import UpdateNotifications,DeleteNotifications
from django.conf.urls.static import static
from django.conf import settings




app_name='mainapp'

urlpatterns = [
        # path('admin_page/',views.admin_page,name='admin_page'),
        # path('login/',views.admin_login,name='admin_login'),
        path('admin_page/',HostelList.as_view(),name='admin_page'),
        path('',NotificationList.as_view(),name='index'),
        path('profile/',views.profile,name='profile'),
        path('newstudent/',CreateStudent.as_view(),name='new_student'),
        path('studentlist/',StudentList.as_view(),name='student_list'),
        path('studentprofile/<int:pk>',StudentProfile.as_view(),name='student_profile'),
        path('hostel_list/<int:pk>',HostelWiseStudentList.as_view(),name='hostel_wise_list'),
        path('bill/<int:pk>',PayFee.as_view(),name='pay_fee'),

        path('notifications/create/',NotificationCreate.as_view(),name='new_notification'),
        path('admin_page/notifications',ManageNotifications.as_view(),name='manage_notification'),
        path('admin_page/notifications/<int:pk>',UpdateNotifications.as_view(),name='update_notification'),
        path('admin_page/notifications/delete/<int:pk>',DeleteNotifications.as_view(),name='delete_notification'),


        path('studentprofile/<int:pk>/fees',AddFees.as_view(),name='add_fees'),









]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
