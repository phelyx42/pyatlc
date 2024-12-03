from PIL import Image, ImageDraw, ImageOps
import re
import pandas as pd
import subprocess

u = int(2)
# Define the image size, base unit it nm

hsub = 100 * u
width, height = 200 * u, hsub * 2
th = 1 * u
track1 = 10 * u
track2 = 2 * u
sep = 2  * u
gap = (track1 + track2 + sep) / 2 * 1
er = 11

# Create a new image with white background (RGB: 255, 255, 255)
image = Image.new("RGB", (width, height), (255, 255, 255))
# Create a drawing object to draw on the image
draw = ImageDraw.Draw(image)

# define substrate
draw.rectangle([0, 0, width, hsub - 1], fill=(200, 200, 200))
# define left GND
draw.rectangle(
    [0, hsub, width / 2 - sep / 2 - track1 - gap, hsub + th], fill=(0, 255, 0)
)

# define left track, track1
draw.rectangle(
    [width / 2 - sep / 2 - track1, hsub, width / 2 - sep / 2, hsub + th],
    fill=(255, 0, 0),
)
# define right track, track 2
draw.rectangle(
    [width / 2 + sep / 2, hsub, width / 2 + sep / 2 + track2, hsub + th],
    fill=(0, 0, 255),
)

# define right GND
draw.rectangle(
    [width / 2 + sep / 2 + track2 + gap, hsub, width, hsub + th], fill=(0, 255, 0)
)
# Save the image as a 24-bit BMP file
image = ImageOps.flip(image)
image.save("output.bmp", "BMP")

print("simulating ..")

result = subprocess.run(
    f"atlc -d c8c8c8={er} output.bmp", shell=True, capture_output=True, text=True
)
pattern = r"(\w+)=\s*([\d\.\-]+)"
matches = re.findall(pattern, result.stdout)

# Convert matches into a dictionary
data = dict(matches)

# Optionally, add any additional data you may need (e.g., filename or version)
data["filename"] = "output.bmp"
data["version"] = "4.6.1"

# Create a pandas DataFrame (you can add more rows if needed)
df = pd.DataFrame([data])
print(df)
