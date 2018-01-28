# run this script in the main src folder: python news/scraper.py

import re
from collections import OrderedDict

import requests
from bs4 import BeautifulSoup
from datetime import datetime

# Setup django to get access to database
import os
import sys
import django

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "totalimpulse.settings.base")
django.setup()

from news.models import NewsPost

# Start scraping news posts
companies = OrderedDict([
    ('Aerojet', 'http://www.rocket.com/content/aerojet-news'),
    ('Accion', 'https://www.accion-systems.com/news/'),
    ('ECAPS', 'http://ecaps.space/category/news/'),
    ('VACCO', 'http://www.cubesat-propulsion.com/blog-news/')
])

for i in range(len(companies)):
	source = list(companies.values())[i]

	page = requests.get(source)

	soup = BeautifulSoup(page.text, 'html.parser')

	# Scrape titles & links from pages
	if list(companies.keys())[i] == 'Aerojet':

		titles = soup.find_all(href = re.compile("article"))

		pre_url = 'http://www.rocket.com'

	elif list(companies.keys())[i] == 'Accion':

		titles = soup.find_all('h1', class_ = 'entry-title')

		dates = soup.find_all('time', class_ = 'published')

		pre_url = 'https://www.accion-systems.com'
	
	elif list(companies.keys())[i] == 'ECAPS':

		titles = soup.find_all('h2', class_ = 'entry-title')

		dates = soup.find_all('time', class_ = 'entry-date published updated')

		pre_url = ''

	elif list(companies.keys())[i] == 'VACCO':

		titles = soup.find_all('h2', class_='entry-title')

		dates = soup.find_all('time', class_='entry-date published')

		pre_url = ''

	# Create entires in database
	for j in range(len(titles)):

		# every site has the href buried differently...
		if list(companies.keys())[i] == 'Aerojet':

			obj, created = NewsPost.objects.update_or_create(
			    company_name = 'Aerojet',
			    title = titles[j].text,
			    url = pre_url + titles[j].get('href'),
			    sector = 'In-Space',
			    tech = 'Hydrazine', 
			    category = 'Chemical',

			)

		elif list(companies.keys())[i] == 'Accion':

			obj, created = NewsPost.objects.update_or_create(
			    company_name = 'Accion',
			    title = titles[j].text,
			    url = pre_url + titles[j].findChildren()[0].get('href'),
			    sector = 'In-Space',
			    tech = 'Electrospray', 
			    category = 'EP',
			    published = dates[j].get('datetime')
			)

		elif list(companies.keys())[i] == 'ECAPS':

			obj, created = NewsPost.objects.update_or_create(
			    company_name = 'Bradford-ECAPS',
			    title = titles[j].text,
			    url = pre_url + titles[j].findChildren()[0].get('href'),
			    sector = 'In-Space',
			    tech = 'ADN', 
			    category = 'Chemical',
			    published = datetime.strptime(dates[j].text, '%B %d, %Y')
			)

		elif list(companies.keys())[i] == 'VACCO':

			obj, created = NewsPost.objects.update_or_create(
			    company_name = 'VACCO',
			    title = titles[j].text,
			    url = pre_url + titles[j].findChildren()[0].get('href'),
			    sector = 'In-Space',
			    tech = 'Cold Gas', 
			    category = 'Chemical',
			    published = datetime.strptime(dates[j].text, '%B %d, %Y')
			)