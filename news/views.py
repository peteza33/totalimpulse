from django.shortcuts import render

from .models import NewsPost

def links(request):

	# latest
	latest = NewsPost.objects.all().order_by('-published')[:10]

	# find original names are in the database
	companies = NewsPost.objects.all().distinct('company_name')

	"""
	filter by each company (probably a better way to do this but....)
	"""
	aerojet = NewsPost.objects.filter(company_name__exact = 'Aerojet').order_by('created')

	accion = NewsPost.objects.filter(company_name__exact = 'Accion').order_by('-published')

	ecaps = NewsPost.objects.filter(company_name__exact = 'Bradford-ECAPS').order_by('-published')

	return render(request, 'news.html', {
		'latest': latest,
		'companies': companies,
		'aerojet': aerojet,
		'accion': accion,
		'ecaps': ecaps,
		})

	# change all the 'create' to 'published' and the scraper is updated