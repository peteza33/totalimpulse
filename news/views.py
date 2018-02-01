from django.shortcuts import render

from .models import NewsPost

def prop_news(request):

	# get entries
	posts = NewsPost.objects.all()

	# latest
	most_recent =posts.order_by('-published')[:10]

	# find original names are in the database
	companies = posts.distinct('company_name')

	"""
	filter by each company 
	"""
	aerojet = posts.filter(company_name__exact = 'Aerojet').order_by('-published')

	accion = posts.filter(company_name__exact = 'Accion').order_by('-published')

	ecaps = posts.filter(company_name__exact = 'Bradford-ECAPS').order_by('-published')

	vacco = posts.filter(company_name__exact = 'VACCO').order_by('-published')

	moog = posts.filter(company_name__exact = 'Moog').order_by('-published')

	return render(request, 'prop_news.html', {
		'most_recent': most_recent,
		'companies': companies,
		'aerojet': aerojet,
		'accion': accion,
		'ecaps': ecaps,
		'vacco': vacco,
		'moog': moog,
		})

def sat_news(request):
	return render(request, 'sat_news.html', {})