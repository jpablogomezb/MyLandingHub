from django.contrib import admin
from django.urls import path
from .views import (
	virtualroom_page,
	#VirtualRoomPageDetailView,
	VirtualRoomPageListView,
	VirtualRoomPageCreateView,
	VirtualRoomPageUpdateView,
	VirtualRoomMaterialUploadView,
	VirtualRoomPageDeleteView,
)

from .ajax import (
    delete_session_material_post,
    inactive_session_material_post,
    active_session_material_post,
)

app_name = 'virtualrooms'
urlpatterns = [
    #path('', landing_list_view, name='landing-list'),
    path('all/', VirtualRoomPageListView.as_view() , name='virtualroom-list'),
    #path('create/', landing_create_view, name='landing-create'),
    path('create/', VirtualRoomPageCreateView.as_view(), name='virtualroom-create'),
    path('<int:pk>/edit/', VirtualRoomPageUpdateView.as_view(), name='virtualroom-update'),
    path('<int:pk>/upload/material/', VirtualRoomMaterialUploadView.as_view(), name='virtualroom-materials'),
    path('<int:pk>/delete/', VirtualRoomPageDeleteView.as_view(), name='virtualroom-delete'),
    path('<slug:slug>/', virtualroom_page, name='virtualroom-detail'),
    #path('<slug:slug>/', LandingPageDetailView.as_view(), name='landing-detail'),
    path('active/material/', active_session_material_post, name='ajax-active-session-material'),
    path('inactive/material/', inactive_session_material_post, name='ajax-inactive-session-material'),
    path('delete/material/', delete_session_material_post, name='ajax-delete-session-material'),
]