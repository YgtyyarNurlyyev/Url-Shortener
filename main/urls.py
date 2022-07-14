from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views
from .views import CustomLoginView, Register, HistoryList

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:link>', views.redirect_url, name='redirect_url'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='index'), name='logout'),
    path('register/', Register.as_view(), name='register'),
    path('tasks/', HistoryList.as_view(), name='urls'),
]
