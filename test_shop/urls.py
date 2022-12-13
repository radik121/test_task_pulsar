from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from shop.views import ProductViewSet

router = DefaultRouter()
router.register('product', ProductViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('shop.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
