"""td_biblio urls"""

from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url('^admin/', admin.site.urls),
    url('^auth/', include('django.contrib.auth.urls')),
    url('^', include('td_biblio.urls', namespace='td_biblio')),
]
