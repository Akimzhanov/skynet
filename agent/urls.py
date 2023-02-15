from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import AgentViewSet, SupervizerViewSet


router = DefaultRouter()
router.register('agent', AgentViewSet, 'agent')
router.register('supervizer', SupervizerViewSet, 'supervizer')

urlpatterns = [

]


urlpatterns += router.urls






