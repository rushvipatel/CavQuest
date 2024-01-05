from django.urls import path
from django.contrib import admin
from . import views
from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView, LoginView

app_name = 'CavQuest_app'
urlpatterns = [
    path('', views.index, name='index'),
    path('homepage_loggedin/', views.homepage_loggedin , name='homepage_loggedin'),
    path("add_tasks/", views.add, name="add_tasks"),
    path('login/', views.login, name='login'),
    path('logout/', views.logout_view, name='logout_view'),
    path('user_profile/', views.user_profile, name='user_profile'),
    path('admin_profile/', views.admin, name='admin_profile'),
    path('task_list/', views.task_list, name='task_list'),
    path('task_list/<int:task_id>/', views.task_details, name='task_details'),
    path('display_submissions/',views.display_submissions,name='display_submissions'),
    path('display_submissions/<int:submission_id>/', views.submission_details, name='submission_details'),
    path('delete_task/<int:task_id>/', views.delete_task, name='delete_task'),
    path('deny-submission/<int:submission_id>/', views.deny_submission, name='deny_submission'),
    path('tutorial/', views.tutorial, name='tutorial'),
    path('user_profile2/', views.user_profile2, name='user_profile2'),
    path('hunting/<int:task_id>/', views.hunting, name='hunting'),
    path('congratulations/<int:task_id>/', views.congratulations, name='congratulations'),
    path('congratulations/', views.congratulations, name='congratulations'),
    path('change_username/', views.change_username, name='change_username'),
    path('about/', views.about, name='about'),
    path('start_task/<int:task_id>/', views.start_task, name='start_task'),
    path('task/<int:task_id>/upload_image/', views.upload_task_image, name='upload_task_image'),

]

