import os

from PIL import Image, ImageDraw, ImageOps

u = int(1)
# Define the image size, base unit it nm

hsub = 200 * u
width, height = 100 * u, hsub * 2
th = 1 * u
track = 20 * u
gap = 10 * u
er = 11

# Create a new image with white background (RGB: 255, 255, 255)
image = Image.new("RGB", (width, height), (255, 255, 255))
# Create a drawing object to draw on the image
draw = ImageDraw.Draw(image)

# define substrate
draw.rectangle([0, 0, width, hsub - 1], fill=(200, 200, 200))

# define left GND
draw.rectangle([0, hsub, width / 2 - track / 2 - gap, hsub + th], fill=(0, 255, 0))

# define left track, track1+sep+track2
draw.rectangle(
    [width / 2 - track / 2, hsub, width / 2 + track / 2, hsub + th], fill=(255, 0, 0)
)

# define right GND
draw.rectangle([width / 2 + gap + track / 2, hsub, width, hsub + th], fill=(0, 255, 0))
# Save the image as a 24-bit BMP file
image = ImageOps.flip(image)
image.save("output.bmp", "BMP")

print("simulating ..")

os.system(f"atlc -d c8c8c8={er} output.bmp ")
