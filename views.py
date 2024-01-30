from django.shortcuts import render

# Create your views here.
import os
import csv
from PIL import Image
from django.http import JsonResponse
from django.contrib import messages
from dice_app.forms import DiceForm
from dice_app.dice_image import DiceImage
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponseBadRequest
from django.http import QueryDict
from django.conf import settings

# temporarily exempt from CSRF protection
## from django.views.decorators.csrf import csrf_exempt

## @csrf_exempt
@csrf_protect
def generate_dice_image(request):
    # print('POST data:', request.POST)  # Add this line for debugging
    # print('Files:', request.FILES)  # Add this line for debugging

    form = DiceForm(request.POST, request.FILES)
    if request.method == 'POST' and form.is_valid():
        # print('Form is valid!')

        # Remove the CSRF token from the cleaned_data dictionary
        # cleaned_data = form.cleaned_data.copy()
        # del cleaned_data['csrfmiddlewaretoken']

        # Get the uploaded image file and dice size from the form
        image_file = request.FILES['image-upload']
        # print('Cleaned image file:', image_file)
        #dice_size = request.POST['dice-size']
        # print('cleaned dice size:',dice_size)

        # Generate the dice-based image and CSV file using the DiceImage class
        #dice_size = request.POST.get('dice-size')
        dice_image = DiceImage(image_file=image_file)
        image = dice_image.generate_dice_image()

        # Get the paths to the generated files
        csv_data = dice_image.get_csv_data()

        # Return the paths to the generated files as a JSON object
        return JsonResponse({'image': image, 'instructions': csv_data})
    else:
        # Form is invalid, handle the errors
        errors = form.errors.as_data()
        for field, error_list in errors.items():
            # Print the field name and the associated error message(s)
            print(f"Field: {field}")
            for error in error_list:
                messages.error(request, error)
                print(f"Error: {error}")
        
        return HttpResponseBadRequest(error_list[0])
    
    # Debug output to check if the view is being accessed
    print('Invalid form or request method is not POST')
    
    # If the request method is not POST, or the form is invalid, return a 400 Bad Request error
    return HttpResponseBadRequest('Bad Request')

def toDice(request):
    form = DiceForm()
    return render(request, '2dice.html', {'form': form})

def upload(request):
    return render(request, 'dice_app/upload.html')

def handle_uploaded_file(file, dice_size):
    dice_image = DiceImage()
    dice_image.dice_size = dice_size

    # Generate a unique filename
    filename = f"{uuid.uuid4()}.jpeg"

    # Save the uploaded image to the media directory
    file_path = os.path.join(settings.MEDIA_ROOT, filename)
    with open(file_path, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)

    dice_image.image_filename = filename

    # Generate the dice image and CSV file
    dice_image.generate_dice_image()
    dice_image.generate_csv_file()
