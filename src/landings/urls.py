from django.contrib import admin
from django.urls import path
from landings.views import (
	# landing_list_view, 
	# landing_detail_view, 
	# landing_create_view,
	landing_page,
	#LandingPageDetailView,
	LandingPageListView,
	LandingPageCreateView,
	LandingPageUpdateView,
	LandingPageDeleteView,
)

app_name = 'landings'
urlpatterns = [
    #path('', landing_list_view, name='landing-list'),
    path('all/', LandingPageListView.as_view() , name='landing-list'),
    #path('create/', landing_create_view, name='landing-create'),
    path('create/', LandingPageCreateView.as_view(), name='landing-create'),
    path('<int:pk>/edit/', LandingPageUpdateView.as_view(), name='landing-update'),
    path('<int:pk>/delete/', LandingPageDeleteView.as_view(), name='landing-delete'),
    path('<slug:slug>/', landing_page, name='landing-detail'),
    #path('<slug:slug>/', LandingPageDetailView.as_view(), name='landing-detail'),
]