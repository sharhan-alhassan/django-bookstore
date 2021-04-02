
from django.urls import path
from . views import HomePageView, AboutPageView, SettingsPageView

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('about/', AboutPageView.as_view(), name='about'),
    path('settings/', SettingsPageView.as_view(), name='settings')
]