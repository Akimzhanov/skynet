from rest_framework import serializers
from .models import Agent, Supervizer


class SupervizerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supervizer
        fields = '__all__'



class AgentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Agent
        fields = '__all__'

    def to_representation(self, instance):
        try:
            representation = super().to_representation(instance)
            rep = instance.supervizer_surname.supervizer_id
            representation['supervizer'] = rep
        except Supervizer.DoesNotExist:
            return False
        return representation







    

        






