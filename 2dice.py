from PIL import Image

# Open an Image
def open_image(path):
	newImage = Image.open(path)
	return newImage

# Save Image
def save_image(image, path):
	image.save(path, 'png')

# Create a new image with the given size
def create_image(i, j):
	image = Image.new("RGB", (i, j), "white")
	return image

# Get the pixel from the given image
def get_pixel(image, i, j):
	# Inside image bounds?
	width, height = image.size
	if i > width or j > height:
		return None

	# Get Pixel
	pixel = image.getpixel((i, j))
	return pixel

# Create a Grayscale version of the image
def convert_grayscale(image):
	# Get size
	width, height = image.size

	# Create new Image and a Pixel Map
	new = create_image(width, height)
	pixels = new.load()

	# Transform to grayscale
	for i in range(width):
		for j in range(height):
			# Get Pixel
			pixel = get_pixel(image, i, j)

			# Get R, G, B values (This are int from 0 to 255)
			red = pixel[0]
			green = pixel[1]
			blue =  pixel[2]

			# Transform to grayscale
			gray = (red * 0.299) + (green * 0.587) + (blue * 0.114)

			# Set Pixel in new image
			pixels[i, j] = (int(gray), int(gray), int(gray))

	# Return new image
	return new

# Create a Primary Colors version of the image
def convert_dice(image):

	# Get size
	width, height = image.size

	# Create new Image and a Pixel Map
	new = create_image(width, height)
	pixels = new.load()

	i = 0
	j = 0

	# Transform to dice
	while j < height-7:
		while i < width-7:
			# Get saturation
			saturation = 0
			for k in range(7):
				for l in range(7):
					pixel = get_pixel(image, i+l, j+k)
					saturation += pixel[2]
					saturation = saturation/14

			for k in range(7):
				for l in range(7):
					pixels[i+l, j+k] = (255,255,255)

			# Transform to dice
			if saturation > 15.83:
				pixels[i+3, j+3] = (0,0,0)
			elif saturation > 12.67:
				pixels[i+1, j+2] = (0,0,0)
				pixels[i+5, j+4] = (0,0,0)
			elif saturation > 9.5:
				pixels[i+1, j+1] = (0,0,0)
				pixels[i+3, j+3] = (0,0,0)
				pixels[i+5, j+5] = (0,0,0)
			elif saturation > 6.33:
				pixels[i+2, j+2] = (0,0,0)
				pixels[i+2, j+4] = (0,0,0)
				pixels[i+4, j+2] = (0,0,0)
				pixels[i+4, j+4] = (0,0,0)
			elif saturation > 3.17:
				pixels[i+1, j+1] = (0,0,0)
				pixels[i+5, j+1] = (0,0,0)
				pixels[i+3, j+3] = (0,0,0)
				pixels[i+1, j+5] = (0,0,0)
				pixels[i+5, j+5] = (0,0,0)
			else:
				pixels[i+2, j+1] = (0,0,0)
				pixels[i+4, j+1] = (0,0,0)
				pixels[i+2, j+3] = (0,0,0)
				pixels[i+4, j+3] = (0,0,0)
				pixels[i+2, j+5] = (0,0,0)
				pixels[i+4, j+5] = (0,0,0)
			i+=7
		i=0
		j+=7

	# Return new image
	return new

# Main
if __name__ == "__main__":
	# Load Image (JPEG/JPG needs libjpeg to load)
	original = open_image('/home/nathan/Pictures/img_001.png')

	# Convert to Grayscale and save
	new = convert_grayscale(original)
	save_image(new, '/home/nathan/Pictures/gray.png')

	# Load gray image
	gray = open_image('/home/nathan/Pictures/gray.png')

	#Crop and save gray image
	width, height = gray.size
	gray.crop((0,0,width-width%7,height-height%7)).save('/home/nathan/Pictures/gray.png','png')

	# Re-load gray image
	gray = open_image('/home/nathan/Pictures/gray.png')

	# Convert to dice and save
	new = convert_dice(gray)
	save_image(new, '/home/nathan/Pictures/dice.png')

