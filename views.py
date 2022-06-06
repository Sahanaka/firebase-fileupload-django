from django.shortcuts import render
from django.http import HttpResponse
from django.core.files.storage import default_storage
from django.contrib import messages

# Create your views here.

import os
import urllib.parse
from uuid import uuid4

import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage


cred = credentials.Certificate('ADD_SERVICE_ACCOUNT')

firebase_admin.initialize_app(cred, {
    'storageBucket': 'dummy-audio-file-upload.appspot.com'
})

class FirebaseFileUploadService:
    
    def upload(self, file):
        default_storage.save(file.name, file)
        bucket = storage.bucket()
        blob = bucket.blob(file.name)

        token = uuid4()
        metadata = {"firebaseStorageDownloadTokens": token}
        blob.metadata = metadata
        try:
            blob.upload_from_filename(f'../media/{file.name}')
            default_storage.delete(f'../media/{file.name}')
        except Exception as e:
            print("File Upload Error", e)

        return f'https://firebasestorage.googleapis.com/v0/b/{bucket.name}/o/{urllib.parse.quote(blob.name)}?alt=media&token={str(token)}'



def index(request):
    return HttpResponse("Index Request")

def firebase_audio_upload(request):
    if request.method != "POST":
        return
    try:
        file = request.FILES['file']
        print(file)
        if not file:
            print("File Issue")
            return HttpResponse("Error in file!", status=400)
        
        file_uploader = FirebaseFileUploadService()
        public_url = file_uploader.upload(file)
        
        return HttpResponse(public_url, status=200)

    except Exception as e:
        print(e)
        return HttpResponse(f"Server Error!, {e}", status=500)
    
    
    
