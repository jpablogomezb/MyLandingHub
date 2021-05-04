from django.contrib import admin
from .models import MoreInfo

# Register your models here.
class MoreInfoAdmin(admin.ModelAdmin):
	list_display =["__str__", "timestamp"]
	#list_filter = ["activity"]
	#search_fields = ["activity"]
	class Meta:
		model = MoreInfo

admin.site.register(MoreInfo, MoreInfoAdmin)