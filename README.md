# dice-app
A Django app that converts images into dice-based images.

## integration
1. Make sure you have the following modules installed:
+ pillow
+ uuid
+ numpy
+ opencv-python

2. Clone the dice_app repository from your projects root folder.
3. Add 'dice_app' to your list of installed apps in your settings.py file. It should look something like this:
```
INSTALLED_APPS = [
    # your apps
    ...
    
    # dice_app
    'dice_app',
]
```
4. Finally, modify your urls.py file to include the following:
```
urlpatterns = [
    # your urls
    ...
    
    # dice_app urls
    path('upload/', upload, name='upload'),
    path('generate_dice_image/', generate_dice_image, name='generate_dice_image'),
    path('2dice/', toDice, name='2dice'),
    ]
```
