from django.urls import path
from .views import GraphView, get_svg, export_csv

app_name = 'devroom_status'

urlpatterns = [
    path('', GraphView.as_view(), name='graph'),
    path('plot', get_svg, name='plot'),
    path('export', export_csv, name='export')
]
