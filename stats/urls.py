from . import views
from django.urls import path

urlpatterns = [
    path('get-stats',views.stats_summary, name="get_stats")
]
