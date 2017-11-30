from __future__ import absolute_import, unicode_literals

from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings

from wagtail.wagtailcore import urls as wagtail_urls
from wagtail.wagtailadmin import urls as wagtailadmin_urls
from wagtail.wagtaildocs import urls as wagtaildocs_urls
from wagtail.wagtailsearch import urls as wagtailsearch_urls

from totalimpulse import views

from plots import urls as plot_urls

urlpatterns = [
    url(r'^$', views.home, name = 'home'),

    url(r'^django-secret-admin/', include(admin.site.urls)),
    url(r'^blog-secret-admin/', include(wagtailadmin_urls)),
    url(r'^search/', include(wagtailsearch_urls)),
    url(r'^documents/', include(wagtaildocs_urls)),

    url(r'^blog/', include(wagtail_urls)),
    url(r'^plots/', include(plot_urls)),
]

# if settings.DEBUG:
#     from django.contrib.staticfiles.urls import staticfiles_urlpatterns

#     urlpatterns += staticfiles_urlpatterns() # tell gunicorn where static files are in dev mode
#     urlpatterns += static(settings.MEDIA_URL + 'images/', document_root=os.path.join(settings.MEDIA_ROOT, 'images'))
#     urlpatterns += [
#         url(r'^favicon\.ico$', RedirectView.as_view(url=settings.STATIC_URL + 'blog/images/favicon.ico'))
#     ]

if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)