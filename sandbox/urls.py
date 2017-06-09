"""td_biblio urls"""

from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('td_biblio.urls', namespace='td_biblio')),
]
