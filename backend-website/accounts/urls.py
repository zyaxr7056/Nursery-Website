from django.urls import path,include
from .views import home,display,SpecificPlant
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('',home, name='home'),
    path('display/', display, name='display'),
    path('display/<int:plant_id>/', SpecificPlant, name='SpecificPlant'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
