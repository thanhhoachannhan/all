from django.contrib import admin
from django.urls import path, include
from django.shortcuts import HttpResponse
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns


urlpatterns = [
    path('', lambda request: HttpResponse('core'), name='index'),
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),
    path('api/', include('api')),
]
urlpatterns += i18n_patterns(
    *[path(f'{app}/', include(f'{app}.urls')) for app in settings.APPS],
    prefix_default_language = False
)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
