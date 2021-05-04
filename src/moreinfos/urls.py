from django.contrib import admin
from django.urls import path
from .views import MoreInfoListView

app_name = 'moreinfos'
urlpatterns = [
    path('<int:pk>/list/', MoreInfoListView.as_view(), name='moreinfo-list'),
  
]