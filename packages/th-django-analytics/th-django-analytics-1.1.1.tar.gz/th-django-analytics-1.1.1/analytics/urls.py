from django.urls import path
from analytics.views import AnalyticView, JinjaView

urlpatterns = [
    path("", AnalyticView.dashboard),
    path("<str:dashId>", AnalyticView.dashboard),
    path("jinja/render/", JinjaView.render)
]
