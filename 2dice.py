from PIL import Image
import sys

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
	new = create_image(width*7, height*7)
	pixels = new.load()

	i = 0
	j = 0
	maxSaturation = 0
	count = 0

	while i < height:
		while j < width:
			pixel = get_pixel(image,i,j)
			if pixel[2] > maxSaturation:
				maxSaturation = pixel[2]
			count += 1
			j+=1
		i+=1

	i = 0
	j = 0

	# Transform to dice
	while j < height:
		while i < width:
			# Get saturation
			saturation = 0
			pixel = get_pixel(image, i, j)
			saturation += pixel[2]

			for k in range(7):
				for l in range(7):
					pixels[(i*7)+l, (j*7)+k] = (255,255,255)

			# Transform to dice
			if saturation > maxSaturation*(5/6):
				pixels[(i*7)+3, (j*7)+3] = (0,0,0)
			elif saturation > maxSaturation*(2/3):
				pixels[(i*7)+1, (j*7)+2] = (0,0,0)
				pixels[(i*7)+5, (j*7)+4] = (0,0,0)
			elif saturation > maxSaturation*(1/2):
				pixels[(i*7)+1, (j*7)+1] = (0,0,0)
				pixels[(i*7)+3, (j*7)+3] = (0,0,0)
				pixels[(i*7)+5, (j*7)+5] = (0,0,0)
			elif saturation > maxSaturation*(1/3):
				pixels[(i*7)+2, (j*7)+2] = (0,0,0)
				pixels[(i*7)+2, (j*7)+4] = (0,0,0)
				pixels[(i*7)+4, (j*7)+2] = (0,0,0)
				pixels[(i*7)+4, (j*7)+4] = (0,0,0)
			elif saturation > maxSaturation*(1/6):
				pixels[(i*7)+1, (j*7)+1] = (0,0,0)
				pixels[(i*7)+5, (j*7)+1] = (0,0,0)
				pixels[(i*7)+3, (j*7)+3] = (0,0,0)
				pixels[(i*7)+1, (j*7)+5] = (0,0,0)
				pixels[(i*7)+5, (j*7)+5] = (0,0,0)
			else:
				pixels[(i*7)+2, (j*7)+1] = (0,0,0)
				pixels[(i*7)+4, (j*7)+1] = (0,0,0)
				pixels[(i*7)+2, (j*7)+3] = (0,0,0)
				pixels[(i*7)+4, (j*7)+3] = (0,0,0)
				pixels[(i*7)+2, (j*7)+5] = (0,0,0)
				pixels[(i*7)+4, (j*7)+5] = (0,0,0)
			i+=1
		i=0
		j+=1

	# Return new image
	return new

# Main
if __name__ == "__main__":
	try:
		# process input
		input = sys.argv[1].split("/")
		file = input[-1]
		path = "/"
		for i in range(len(input)-1):
			path += input[i] + "/"

		# Load Image (JPEG/JPG needs libjpeg to load)
		original = open_image(path + file)

		if file.split(".")[1] != "png":
			raise Exception("Sorry, png images only! Please convert your image to png and try again.")
			sys.exit()

		# Convert to Grayscale and save
		new = convert_grayscale(original)
		save_image(new, path + 'gray.png')

		# Load gray image
		gray = open_image(path + 'gray.png')

		# Convert to dice and save
		new = convert_dice(gray)
		save_image(new, path + 'dice.png')

	except FileNotFoundError:
		print("File not found. Please make sure your path and file name are correct and try again.")


