from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from upt_v2.flower import FlowerProxyView

urlpatterns = [
    path('', include('main.urls')),
    FlowerProxyView.as_url(),
    path('admin/', admin.site.urls),
    path('account/', include('accounts.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
