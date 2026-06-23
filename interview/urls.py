from django.contrib import admin
from django.urls import path
from django.urls import include
from config import settings
from interview import views
from django.conf.urls.static import static

from interview import views

urlpatterns = [
    path('', views.index, name='index'),
    path('userReg/', views.userReg, name='userReg'),
    path('login/', views.login_view, name='login'),

    path('adminhome/', views.adminhome, name='adminhome'),
    path('add_question/', views.add_question, name='add_question'),

    path('uhome/', views.uhome, name='uhome'),
    path('select-category/',views.select_category,name='select_category'),
    path('start-interview/<int:cid>/',views.start_interview,name='start_interview'),
    path('detect-face/',views.detect_face,name='detect_face'),
    path('malpractice/',views.malpractice,name='malpractice'),
    path('request-interview/<int:cid>/',views.request_interview,name='request_interview'),
    path('view-requests/',views.view_requests,name='view_requests'),
    path('view-results/',views.view_results,name='view_results'),
    path('approve-request/<int:req_id>/',views.approve_request,name='approve_request'),
    path('reject-request/<int:req_id>/',views.reject_request,name='reject_request'),
    path('malpractice-detected/',views.malpractice_detected,name='malpractice_detected'), 
    path('user_view_results/',views.user_view_results,name='user_view_results'), 
    

]+static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)