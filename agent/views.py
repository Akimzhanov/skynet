from rest_framework.viewsets import mixins, GenericViewSet
from rest_framework.permissions import AllowAny, IsAdminUser
from .models import Agent, Supervizer
from .serializers import AgentSerializer, SupervizerSerializer
 


class AgentViewSet(mixins.CreateModelMixin,
                    mixins.DestroyModelMixin,
                    mixins.ListModelMixin,
                    mixins.UpdateModelMixin,
                    GenericViewSet):
                
    queryset = Agent.objects.all()
    serializer_class = AgentSerializer


    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [AllowAny]
        if self.action in ['destroy', 'update', 'partail_update']:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()







class SupervizerViewSet(mixins.CreateModelMixin,
                            mixins.DestroyModelMixin,
                            mixins.UpdateModelMixin,
                            mixins.ListModelMixin,
                            GenericViewSet):
    queryset = Supervizer.objects.all()
    serializer_class = SupervizerSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'destroy', 'update', 'partial_update']:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()









