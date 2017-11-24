from django.shortcuts import render

# Home page. Passes the top voted tickets for each category to the template
def home(request):
	return render(request, 'home.html', {})

def about(request):
	return render(request, 'about.html', {})