from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.files.storage import FileSystemStorage
import base64
import cv2
import numpy as np

# Create your views here.
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

def profile(request):
    abd_image_url = None
    morphologic_image_url = None
    blood_type = None
    if request.method == 'POST':
        abd_image = request.FILES.get('abd_image')
        if abd_image:
            fs = FileSystemStorage()
            filename = fs.save(abd_image.name, abd_image)
            uploaded_file_url = fs.url(filename)

            img = cv2.imread(fs.path(filename))

            # Step 1: Convert to grayscale
            gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            # Step 2: Apply Gaussian blur to reduce noise
            blur_img = cv2.GaussianBlur(gray_img, (5, 5), 0)

            # Step 3: Enhance the contrast of the image
            enhance_img = cv2.equalizeHist(blur_img)

            # Step 4: Apply Otsu's thresholding
            _, bin_img = cv2.threshold(enhance_img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

            # Step 5: Perform morphological operations
            kernel_imp = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
            bin_img = cv2.morphologyEx(bin_img, cv2.MORPH_OPEN, kernel_imp)  # Remove small noise
            bin_img = cv2.morphologyEx(bin_img, cv2.MORPH_CLOSE, kernel_imp)  # Fill small holes

            # Encode the morphologically processed image to base64
            _, morphologic_buffer = cv2.imencode('.jpg', bin_img)
            morphologic_encoded = base64.b64encode(morphologic_buffer).decode('utf-8')
            morphologic_image_url = f"data:image/jpg;base64,{morphologic_encoded}"

            # Base64 encoding for original image
            _, buffer = cv2.imencode('.jpg', img)
            encoded_image = base64.b64encode(buffer).decode('utf-8')
            abd_image_url = f"data:image/jpg;base64,{encoded_image}"

            # Calculate blood type
            hei, wid = bin_img.shape
            mid_wid = wid // 3

            region_A = bin_img[:, 0:mid_wid]
            region_B = bin_img[:, mid_wid:2 * mid_wid]
            region_D = bin_img[:, 2 * mid_wid:]

            # Define agglutination calculation
            def cal_agg(region):
                num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(region, connectivity=8)
                return num_labels - 1

            # Calculate connected components in each region
            num_region_A = cal_agg(region_A)
            num_region_B = cal_agg(region_B)
            num_region_D = cal_agg(region_D)

            # Determine the blood type based on agglutination
            if num_region_A > 0 and num_region_B == 0 and num_region_D > 0:
                blood_type = "A+"
            elif num_region_A == 0 and num_region_B > 0 and num_region_D > 0:
                blood_type = "B+"
            elif num_region_A > 0 and num_region_B > 0 and num_region_D > 0:
                blood_type = "AB+"
            elif num_region_A == 0 and num_region_B == 0 and num_region_D > 0:
                blood_type = "O+"
            elif num_region_A > 0 and num_region_B == 0 and num_region_D <= 0:
                blood_type = "A-"
            elif num_region_A == 0 and num_region_B > 0 and num_region_D <= 0:
                blood_type = "B-"
            elif num_region_A > 0 and num_region_B > 0 and num_region_D <= 0:
                blood_type = "AB-"
            elif num_region_A == 0 and num_region_B == 0 and num_region_D <= 0:
                blood_type = "O-"
            else:
                blood_type = "Unknown"
        else:
            return render(request, "profile.html", {
                'error_message': "Please upload ABD blood cell images."
            })

    return render(request, 'profile.html', {
        'abd_image_url': abd_image_url,
        'morphologic_image_url': morphologic_image_url,
        'blood_type': blood_type
    })
