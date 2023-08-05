from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

app_name = "syngo"
urlpatterns = [
    path("captcha/", views.generate, name="generate"),
    path("captcha/<int:pk>", views.check, name="check"),
]
if settings.DEBUG:  # pragma: no cover
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
