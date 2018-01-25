from django.shortcuts import render

def latest_news(request):
	return render(request, 'news.html', {})