from django.contrib import admin

from .models import VirtualRoomPage, SessionMaterial, AttendeeVroom
# Register your models here.
admin.site.register(VirtualRoomPage)
admin.site.register(SessionMaterial)

class AttendeeVroomAdmin(admin.ModelAdmin):
	list_display =["__str__", "timestamp"]
	class Meta:
		model = AttendeeVroom

admin.site.register(AttendeeVroom, AttendeeVroomAdmin)