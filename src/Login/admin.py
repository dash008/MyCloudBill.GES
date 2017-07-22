from django.contrib import admin
from .models import UserProfile
from .forms import UserForm
# Register your models here.

class UserAdmin(admin.ModelAdmin):
	list_display = ["__str__", "password"]
	form = UserForm
#	class Meta:
#		model =  User

admin.site.register(UserProfile)