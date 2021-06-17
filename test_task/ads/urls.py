from django.urls import path
from ads.views import AdView

urlpatterns = [
    path('', AdView.as_view())
]
