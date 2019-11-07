from django.shortcuts import render
from django.template.response import TemplateResponse

# Create your views here.
def home(request):
	# Close session when page is loaded
	request.session.flush()

	return TemplateResponse(request, 'home.html')