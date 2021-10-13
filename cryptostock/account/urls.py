from account.views import BrokerViewSet, ClientViewSet
from market.views import MarketViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register("markets", MarketViewSet)
router.register("brokers", BrokerViewSet)
router.register("clients", ClientViewSet)

urlpatterns = router.urls
