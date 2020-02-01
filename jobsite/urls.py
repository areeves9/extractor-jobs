"""jobsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf import settings
# from django.conf.urls import include, url
from django.urls import include, re_path

from django.conf.urls.static import static
from django.contrib import admin


from utils.autocomplete import CityAutocomplete


urlpatterns = [
    re_path('admin/', admin.site.urls),
    re_path('accounts/', include(('accounts.urls', 'accounts'), namespace='accounts')),
    re_path('account/', include(('django.contrib.auth.urls', 'django.contrib.auth'), namespace='account')),
    re_path('jobs/', include(('jobs.urls', 'jobs'), namespace='jobs')),
]

if settings.DEBUG is True:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
