import datetime

from django import forms

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class DiceForm(forms.Form):
    image_upload = forms.ImageField(required=False)
    dice_size = forms.ChoiceField(
        choices=[('20', '20x20'), ('30', '30x30'), ('40', '40x40')],
        required=False
    )

    def clean_image_upload(self):
        image_file = self.files.get('image-upload')
        print('Cleaned image file:', image_file)
        if not image_file:
            raise forms.ValidationError('No image file selected.')
        if image_file.file is None:
            raise forms.ValidationError('Error uploading the image file.')
        return image_file