from django.contrib import admin
from django.urls import path
from .views import (
	NewsletterSignupView,
	NewsletterSignupListView,
)

app_name = 'signups'
urlpatterns = [
    path('<int:pk>/signup/', NewsletterSignupView.as_view(), name='newsletter-signup'),
    path('<int:pk>/subscriptions/', NewsletterSignupListView.as_view(), name='newsletter-subscriptions'),
  
]