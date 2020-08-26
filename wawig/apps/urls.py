from django.urls        import path
from .views             import WaWiGView

app_name = 'wawig'

urlpatterns = [
    path('', WaWiGView.as_view(), name='search_city')
]
