from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),

    # path('recruiter-home', views.recruiter_home, name="recruiter-home"),
    path('recruiter-login', views.recruiter_login, name="recruiter-login"),
    path('recruiter-signup', views.recruiter_signup, name="recruiter-signup"),
    path('add-jobs', views.add_jobs, name="add-jobs"),
    path('job-list', views.job_list, name="job-list"),
    path('update-job/<int:myid>', views.update_job, name="update-job"),
    path('delete-job/<int:id>', views.delete_job, name="delete-job"),
    path('recruiter-profile', views.recruiter_profile, name="recruiter-profile"),
    path('update-recruiter/<int:id>', views.update_recruiter, name="update-recruiter"),
    path('show-apply-candidate', views.show_apply_candidate, name="show-apply-candidate"),
    path('delete-candidate/<int:id>', views.delete_candidate, name="delete-candidate"),
    # path('recruiter-logout', views.recruiter_logout, name="recruiter-logout"),

    path('user-signup', views.user_signup, name="user-signup"),
    path('user-login', views.user_login, name="user-login"),
    path('user-logout', views.user_logout, name="user-logout"),
    path('user-profile', views.user_profile, name="user-profile"),
    path('user-update/<int:id>', views.user_update, name="user-update"),
    path('user-joblist', views.user_joblist, name="user-joblist"),
    path('job-details/<int:id>', views.job_details, name="job-details"),
    path('apply-job/<int:id>', views.apply_job, name="apply-job"),
    path('show-user-application', views.show_user_application, name="show-user-application"),
    path('job-search', views.job_search, name="job-search"),

    path('admin-login', views.admin_login, name="admin-login"),
    path('admin-home', views.admin_home, name="admin-home"),
    path('admin-delete-job/<int:id>', views.admin_delete_job, name="admin-delete-job"),
    path('view-users', views.view_users, name="view-users"),
    path('delete-user/<int:id>', views.delete_user, name="delete-user"),
    path('recruiter-pending', views.recruiter_pending, name="recruiter-pending"),
    path('change-status/<int:id>', views.change_status, name="change-status"),
    path('recruiter-rejected', views.recruiter_rejected, name="recruiter-rejected"),
    path('recruiter-accepted', views.recruiter_accepted, name="recruiter-accepted"),
    path('all-recruiter', views.all_recruiter, name="all-recruiter"),
    path('delete-recruiter/<int:id>', views.delete_recruiter, name="delete-recruiter"),
    path('admin-logout', views.admin_logout, name="admin-logout"),


    path('job/<int:job_id>/send-message/', views.send_message, name='send-message'),
    path('job/<int:job_id>/messages/', views.job_messages, name='job-messages'),
]
