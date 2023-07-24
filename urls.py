from django.urls import path
from . import views


# ========== Tracker-application-url-patterns ==========

urlpatterns = [
    path('', views.home,name='home'),
    path('quest/',views.task,name='quest'),
    path('viewtask/', views.viewtask, name='viewtask'),
    path('viewdev/', views.viewdev, name='viewdev'),
    path('deletedev/<int:id>', views.deletedev, name='deletedev'),
    path('update/<int:id>', views.updatetask, name='update'),
    path('delete/<int:id>', views.deletetask, name='delete'),
    path('contact', views.contact, name='contact'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup')
]