from django.urls import path
from ._views import ImageResponder

urlpatterns = [
    path('<transform>', ImageResponder.handle, name='dodi_image')
]