from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('fileupload', views.firebase_audio_upload, name='fileupload')
]