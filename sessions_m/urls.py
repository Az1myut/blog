from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('set_cookie/', views.set_cookie, name='set_cookie'),
    path('get_cookie/', views.get_cookie, name='get_cookie'),
    path('delete_cookie/', views.delete_cookie, name='delete_cookie'),
    path('set_session/', views.set_session, name='set_session'),
    path('get_session/', views.get_session, name='get_session'),
    path('delete_session/', views.delete_session, name='delete_session'),
    path('sign_data/', views.sign_data, name='sign_data'),
    path('verify_data/', views.verify_data, name='verify_data'),
    path('class_based/', views.ClassBasedSessionsView.as_view(), name='class_based'),
    path('class_sign/', views.ClassBasedSignView.as_view(), name='class_sign'),
]
