from django.contrib import admin
from .models import Agent, Supervizer


class AgentAdmin(admin.ModelAdmin):
    exclude = ['bx_id', 'supervizer_id', 'supervizer']


admin.site.register(Agent, AgentAdmin)
admin.site.register(Supervizer)




