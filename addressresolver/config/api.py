from rest_framework import routers

from address.views import AddressViewSet

router = routers.DefaultRouter()
router.register(r'address', AddressViewSet, 'address')
