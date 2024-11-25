from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .forms import UploadImageForm
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from PIL import Image
import cv2
import numpy as np

def home(request):
    return render(request, 'home.html')

def login_view(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        un = request.POST['username']
        pw = request.POST['password']
        user = authenticate(request, username=un, password=pw)
        if user is not None:
            return redirect('/profile')
        else:
            msg = 'error'
            form = AuthenticationForm()
            return render(request, 'login.html', {'form': form, 'msg': msg})
    else:
        form = AuthenticationForm()
        return render(request, 'login.html', {'form': form})

def signup_view(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            un = form.cleaned_data.get('username')
            pw = form.cleaned_data.get('password1')
            authenticate(username=un, password=pw)
            return redirect('/login')
        else:
            return render(request, 'signup.html', {'form': form})
    else:
        form = UserCreationForm()
        return render(request, 'signup.html', {'form': form})

from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import cv2
from .forms import UploadImageForm

def profile_view(request):
    if request.method == 'POST':
        form = UploadImageForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the uploaded image to the media directory
            img = form.cleaned_data['abd_image']
            path = default_storage.save('tmp/' + img.name, ContentFile(img.read()))
            img_path = default_storage.path(path)
            img_url = default_storage.url(path)  # Get the URL of the saved image

            bin_img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
            _, bin_img = cv2.threshold(bin_img, 127, 255, cv2.THRESH_BINARY)

            hei, wid = bin_img.shape
            mid_wid = wid // 3
            region_A = bin_img[:mid_wid]
            region_B = bin_img[mid_wid:2*mid_wid]
            region_D = bin_img[2*mid_wid:]

            def cal_agg(region):
                num_labels, labels, stats, var = cv2.connectedComponentsWithStats(region, connectivity=8)
                return num_labels - 1

            num_region_A = cal_agg(region_A)
            num_region_B = cal_agg(region_B)
            num_region_D = cal_agg(region_D)

            # Determine blood group based on contour counts
            blood_group = determine_blood_group(num_region_A, num_region_B, num_region_D)
            print(f"Contour Counts: A={num_region_A}, B={num_region_B}, D={num_region_D}")
            print(f"Determined Blood Group: {blood_group}")

            return render(request, 'profile.html', {
                'abd_image_url': img_url,
                'contour_count': (num_region_A, num_region_B, num_region_D),
                'blood_group': blood_group
            })
    else:
        form = UploadImageForm()

    return render(request, 'profile.html', {'form': form})

def determine_blood_group(num_A, num_B, num_D):
    if num_A > 0 and num_B > 0 and num_D > 0:
        return "AB+"
    elif num_A > 0 and num_B > 0 and num_D == 0:
        return "AB-"
    elif num_A > 0 and num_B == 0 and num_D > 0:
        return "A+"
    elif num_A > 0 and num_B == 0 and num_D == 0:
        return "A-"
    elif num_A == 0 and num_B > 0 and num_D > 0:
        return "B+"
    elif num_A == 0 and num_B > 0 and num_D == 0:
        return "B-"
    elif num_A == 0 and num_B == 0 and num_D > 0:
        return "O+"
    elif num_A == 0 and num_B == 0 and num_D == 0:
        return "O-"
    else:
        return "Unknown"

