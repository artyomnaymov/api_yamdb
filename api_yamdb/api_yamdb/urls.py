from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

from api_yamdb.yasg import urlpatterns as api_doc

urlpatterns = [
    path('api/', include('api.urls')),
    path('admin/', admin.site.urls),
    path(
        'redoc/',
        TemplateView.as_view(template_name='redoc.html'),
        name='redoc'
    ),
]
urlpatterns += api_doc
