from django.contrib import admin

from .models import NewsPost

class NewsPostAdmin(admin.ModelAdmin):
	list_display = ('id', 'company_name', 'title', 'url', 'sector', 'tech', 'category', 'published', 'created', 'modified')

admin.site.register(NewsPost, NewsPostAdmin)