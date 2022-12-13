from rest_framework.routers import DefaultRouter
from shop.views import ProductViewSet

router = DefaultRouter()
router.register('product', ProductViewSet)

urlpatterns = router.urls