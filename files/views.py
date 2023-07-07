from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib import messages
from .models import UserProfile, UserInput
from .forms import UserInputForm
from django.conf import settings
from google.oauth2 import service_account


@login_required
def index(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
        user_inputs = UserInput.objects.all()
        if request.method == 'POST':
            form = UserInputForm(request.POST, request.FILES)
            if form.is_valid():
                user_input = form.save(commit=False)
                user_input.user_profile = request.user.userprofile  # Assign the logged-in user's userprofile
                form.save()
                messages.success(request, 'Form submitted successfully.')
                return redirect('index')  # Redirect to the index page or any other desired page
        else:
            form = UserInputForm()
    except UserProfile.DoesNotExist:
        user_profile = None
        user_inputs = None
    context = {
        'user_profile': user_profile, 
        'form': form, 
        'user_inputs': user_inputs
    }
    
    return render(request, 'index.html', context)


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            error_message = "Invalid login credentials. Please try again."
            return render(request, 'login.html', {'error_message': error_message})
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('index')

from django.http import JsonResponse
from google.cloud import storage

def generate_signed_url(request):
    print("The request Object: ", request)
    print("user_input_id = : ", request.POST.get('user_input_id'))

    if request.method == 'POST':
        user_input_id = request.POST.get('user_input_id')
        try:
            user_input = UserInput.objects.get(id=user_input_id)
            if user_input.file:
                # Generate signed URL for the file
                signed_url = generate_signed_url_for_file(user_input.file.name)
                return JsonResponse({'signed_url': signed_url})
            else:
                return JsonResponse({'error': 'File not found.'}, status=400)
        except UserInput.DoesNotExist:
            return JsonResponse({'error': 'UserInput not found.'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=400)

def generate_signed_url_for_file(file_name):
    credentials = service_account.Credentials.from_service_account_file(
        settings.GOOGLE_APPLICATION_CREDENTIALS,
        scopes=['https://www.googleapis.com/auth/cloud-platform'],
    )
    client = storage.Client(credentials=credentials)
    bucket = client.bucket(settings.GOOGLE_CLOUD_STORAGE_BUCKET)
    blob = bucket.blob(file_name)

    signed_url = blob.generate_signed_url(
        version="v4",
        expiration=3600,  # Adjust the expiration time as needed
        method="GET",
    )
    return signed_url