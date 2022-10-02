from django.contrib import admin

from bidder.models import AgentProfile, Graph, Strategy


admin.site.register(AgentProfile)
admin.site.register(Graph)
admin.site.register(Strategy)
