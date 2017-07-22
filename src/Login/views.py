from django.shortcuts import render
from django.contrib import auth
from .forms import UserForm


# Create your views here.
def home (request):
	title = "Ingreso a la aplicacion"
	form = UserForm(request.POST or None)

	if form.is_valid():
		instance = form.save(commit=False)
		if instance.username == none:
			instance.username = ""
		print (instance.username)
	context = {
		"template_title":title,
		"form": form	
	}
	return render(request, "home.html", context)

