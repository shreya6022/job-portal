from django.urls import path
from . import views  # Ensure this imports views from the same app
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('', views.home, name='home'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('log/', views.user_login, name='l'),
    path('reg', views.register, name='r'),
    path('spro', views.seekerpro, name='sp'),
    path('cpro', views.creatorpro, name='cp'),
    path('seeker/', views.seeker_profile, name='sv'),
    path('creator/', views.creator_profile, name='cv'),
    path('add-job/', views.addjob, name='a'),
    path('job-list/', views.joblist, name='jl'),
    path('creator/<str:username>/', views.creatordas, name='cdas'),
    path('seeker/<str:username>/', views.seekerdas, name='sdas'),
    path('main-user/', views.mainuser, name='main_user'),
    path('logout/', views.logout_view, name='logout'),
    path("seeker-login/<uuid:job_id>/", views.seeker_login, name="seeker_login"), 
    path("apply-form/<uuid:job_id>/", views.apply_form, name="apply_form"),
    path('show-job', views.showjob, name='sj'),
    path('approve/<int:application_id>/', views.approve_application, name='approve_application'),
    path('reject/<int:application_id>/', views.reject_application, name='reject_application'),
    path('seeker/<str:username>/applied-jobs/', views.showapplyjob, name='seeker_applied_jobs'),
    path('apanel', views.apanel, name='ap'),
    path('allseeker', views.allseeker, name='alls'),
    path('allcreator', views.allcreator, name='allc'),
    path('about', views.about, name='about'),
    path("all-job",views.allapplyjob,name="allj"),
    path('delete-seeker/<uuid:seeker_id>/', views.delete_seeker, name='delete_seeker'),
    path('delete-creator/<uuid:creator_id>/', views.delete_creator, name='delete_creator'),
    path('cont',views.contact,name="con")
]   
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)