from django.urls import path
from accounts import manage_views
from . import views

urlpatterns = [
    path('signup/', views.signup, name='accounts.signup'),
    path('login/', views.login, name='accounts.login'),
    path('logout/', views.logout, name='accounts.logout'),
    path('orders/', views.orders, name='accounts.orders'),
    path('manage/', manage_views.manage, name='accounts.manage'),
    path('manage/engagement/', manage_views.engagement, name='accounts.manage_engagement'),
    path('engagement/', manage_views.engagement, name='accounts.engagement'),
]
