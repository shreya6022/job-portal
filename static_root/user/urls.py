from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from user import views

urlpatterns = [

    path('', views.home, name='home'),
    path('s/', views.mainuser,name='m'),
    path('log/', views.user_login, name='l'),
    path('reg/', views.register, name='r'),
    path('cpro', views.creatorpro, name='cp'),
    path('spro', views.seekerpro, name='sp'),
    path('cv', views.creatorview, name='cv'),
    path('ad', views.addjob, name='a'),
    path('sv', views.seekerview, name='sv'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
