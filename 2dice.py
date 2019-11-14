from PIL import Image
import sys

# Create a Grayscale version of the image
def convert_grayscale(image):
	# Get size
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

	# Return new image
	return new

# Create a Primary Colors version of the image
def convert_dice(image):

	# Get size
	width, height = image.size

	# Create new Image and a Pixel Map
	new = Image.new("RGB", (width*7, height*7), "white")
	pixels = new.load()

	i = 0
	j = 0
	maxSaturation = 0
	count = 0

	while i < height:
		while j < width:
			pixel = image.getpixel((i,j))
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
			pixel = image.getpixel((i,j))
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

def main():
	# process input
	input = sys.argv[1].strip()
	delimiter = ""

	if "/" in input:
		delimiter = "/"
	elif "\\" in input:
		delimiter = "\\"

	input = input.split(delimiter)
	file = input[-1]
	path = ""

	if len(input) != 1:
		path = delimiter

	for i in range(len(input)-1):
		path += input[i] + delimiter

	try:
		# Load Image (JPEG/JPG needs libjpeg to load)
		original = Image.open(path + file)

	except FileNotFoundError:
		print(path + file)
		print("File not found. Please make sure your path and file name are correct and try again.")

	else:
		suffix = "." + file.split(".")[-1]

		# Convert to Grayscale and save
		new = convert_grayscale(original)
		new.save(path + 'gray' + suffix)

		# Load gray image
		gray = Image.open(path + 'gray' + suffix)

		# Convert to dice and save
		new = convert_dice(gray)
		new.save(path + 'dice' + suffix)

if __name__ == "__main__":
	main()