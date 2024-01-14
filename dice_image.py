import os
import csv
from PIL import Image,ImageOps
import tempfile
import uuid
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render, redirect
import numpy as np
import cv2

class DiceImage:
    def __init__(self, image_file):
        self.image_file = image_file
        self.image_filename = None
        self.csv_filename = None

    def generate_dice_image(self):
        size_modifier = 5 # 1, 2, 4, 5, 10, or 20 only
        dice_size = 20

        # Convert the uploaded image file to a PIL Image object
        image = Image.open(self.image_file)
        image = ImageOps.exif_transpose(image)

        # get size
        width, height = image.size

        # # resize image
        # left = 0
        # right = width
        # top = 0
        # bottom = height

        # if width%20 != 0:
        #     if (width%20)%2 == 0:
        #         left = (width%20)/2
        #         right = width - left
        #     else:
        #         left = math.floor((width%20)/2)
        #         right = width - math.ceil((width%20)/2)

        # if height%20 != 0:
        #     if (height%20)%2 == 0:
        #         top = (height%20)/2
        #         bottom = height - top
        #     else:
        #         top = math.floor((height%20)/2)
        #         bottom = height - math.ceil((height%20)/2)

        # image = image.crop((left, top, right, bottom))

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

        csv_data = []

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

            csv_data.append(csv_row)

            i=0
            j+=(dice_size//size_modifier)

        # Save the generated dice-based image
        self.image_filename = f'dice_image_{uuid.uuid4()}.png'
        self.image_path = os.path.join(settings.MEDIA_ROOT, self.image_filename)
        new.save(self.image_path)

        # Generate the CSV file with the dice values
        self.csv_filename = f'dice_image_{uuid.uuid4()}.csv'
        self.csv_path = os.path.join(settings.MEDIA_ROOT, self.csv_filename)
        with open(self.csv_path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(csv_data)

    def get_image_filename(self):
        if self.image_filename is None:
            self.image_filename = f'dice_image_{uuid.uuid4()}.png'
        return self.image_filename

    def get_csv_filename(self):
        if self.csv_filename is None:
            self.csv_filename = f'dice_image_{uuid.uuid4()}.csv'
        return self.csv_filename