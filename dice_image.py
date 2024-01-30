import os
import io
import csv
from PIL import Image,ImageOps
import tempfile
import uuid
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render, redirect
import numpy as np
import cv2
import base64

class DiceImage:
    def __init__(self, image_file):
        self.image_file = image_file
        self.image_filename = None
        self.csv_filename = None
        self.csv_data = []

    def generate_dice_image(self):
        size_modifier = 5
        dice_size = 20

        # Convert the uploaded image file to a PIL Image object
        image = Image.open(self.image_file)
        image = ImageOps.exif_transpose(image)

        # get size
        width, height = image.size

        # Create new Image and a Pixel Map
        new = Image.new("RGB", (width, height), "white")
        pixels = new.load()

        # Transform to grayscale
        for i in range(width):
            for j in range(height):
                # Get Pixel
                pixel = image.getpixel((i,j))

                # Get R, G, B values (This are int from 0 to 255)
                red = pixel[0]
                green = pixel[1]
                blue =  pixel[2]

                # Transform to grayscale
                gray = (red * 0.299) + (green * 0.587) + (blue * 0.114)

                # Set Pixel in new image
                pixels[i, j] = (int(gray), int(gray), int(gray))

        image = new

        # Create a new image to hold the dice-based image
        # Get size
        width, height = image.size

        # Create new Image and a Pixel Map
        dice_size = int(dice_size)
        new = Image.new("RGB", ((width - (width % dice_size))*size_modifier, (height - (height % dice_size))*size_modifier), "white")
        pixels = new.load()

        width, height = new.size

        i = 0
        j = 0
        maxSaturation = 0

        w,h = image.size

        while i < h:
            while j < w:
                pixel = image.getpixel((j,i))
                if pixel[2] > maxSaturation:
                    maxSaturation = pixel[2]
                j+=1
            i+=1
            j=0

        i = 0

        # Load the dice images
        dice_images = []
        for i in range(1, 7):
            dice_image_file = os.path.join(os.path.dirname(__file__), f'dice_images/dice{i}-{dice_size}.png')
            dice_image = Image.open(dice_image_file)
            dice_images.append(dice_image)

        i = 0
        j = 0
        # Transform to dice
        while j < (height/size_modifier):
            csv_row = []
            while i < (width/size_modifier):
                # print(i,j)
                # Get saturation
                saturation = 0
                for m in range(j, j+(dice_size//size_modifier)):
                    for n in range(i, i+(dice_size//size_modifier)):
                        pixel = image.getpixel((n,m))
                        saturation += pixel[2]
                saturation = saturation/((dice_size//size_modifier)**2)

                # Transform to dice
                if saturation > maxSaturation*(5/6):
                    for m in range(0,dice_size):
                        for n in range(0,dice_size):
                            pixels[(i*size_modifier)+n,(j*size_modifier)+m] = dice_images[0].getpixel((n,m))
                    csv_row.append(1)

                elif saturation > maxSaturation*(3/4):
                    for m in range(0,dice_size):
                        for n in range(0,dice_size):
                            pixels[(i*size_modifier)+n,(j*size_modifier)+m] = dice_images[1].getpixel((n,m))
                    csv_row.append(2)

                elif saturation > maxSaturation*(2/3):
                    for m in range(0,dice_size):
                        for n in range(0,dice_size):
                            pixels[(i*size_modifier)+n,(j*size_modifier)+m] = dice_images[2].getpixel((n,m))
                    csv_row.append(3)

                elif saturation > maxSaturation*(1/2):
                    for m in range(0,dice_size):
                        for n in range(0,dice_size):
                            pixels[(i*size_modifier)+n,(j*size_modifier)+m] = dice_images[3].getpixel((n,m))
                    csv_row.append(4)

                elif saturation > maxSaturation*(1/3):
                    for m in range(0,dice_size):
                        for n in range(0,dice_size):
                            pixels[(i*size_modifier)+n,(j*size_modifier)+m] = dice_images[4].getpixel((n,m))
                    csv_row.append(5)

                else:
                    for m in range(0,dice_size):
                        for n in range(0,dice_size):
                            pixels[(i*size_modifier)+n,(j*size_modifier)+m] = dice_images[5].getpixel((n,m))
                    csv_row.append(6)

                i+=(dice_size//size_modifier)

            self.csv_data.append(csv_row)

            i=0
            j+=(dice_size//size_modifier)

        # Return the generated dice-based image
        img_byte_array = io.BytesIO()
        new.save(img_byte_array, format='JPEG', subsampling=0, quality=100)
        img_byte_array = str(base64.b64encode(img_byte_array.getvalue()))
        return img_byte_array

    def get_csv_data(self):
        return str(self.csv_data)
