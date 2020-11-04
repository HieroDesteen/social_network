from rest_framework import routers

from engine.views import PostViewSet

router = routers.DefaultRouter(trailing_slash=True)
router.register('posts', PostViewSet)
urlpatterns = router.urls
