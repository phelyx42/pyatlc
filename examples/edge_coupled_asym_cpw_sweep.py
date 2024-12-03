from PIL import Image, ImageDraw, ImageOps
import re
import pandas as pd
import numpy as np
import subprocess
from tqdm import tqdm

datalist = []

u = int(1)
# Define the image size, base unit it nm
for ti, track2 in tqdm(enumerate(np.linspace(2, 10, 51))):
    for si, sep in enumerate(np.linspace(2, 10, 51)):
        hsub = 100 * u
        width, height = 200 * u, hsub * 2
        th = 1 * u
        track1 = 10 * u
        track2 = track2 * u
        sep = sep * u
        gap = (track1 + track2 + sep) / 2
        er = 11

        # Create a new image with white background (RGB: 255, 255, 255)
        image = Image.new("RGB", (width, height), (255, 255, 255))
        # Create a drawing object to draw on the image
        draw = ImageDraw.Draw(image)

        # define substrate
        draw.rectangle([0, 0, width, hsub - 1], fill=(200, 200, 200))
        # define left GND
        draw.rectangle(
            [0, int(hsub), int(width / 2 - sep / 2 - track1 - gap), int(hsub + th)],
            fill=(0, 255, 0),
        )

        # define left track, track1
        draw.rectangle(
            [
                int(width / 2 - sep / 2 - track1),
                int(hsub),
                int(width / 2 - sep / 2),
                int(hsub + th),
            ],
            fill=(255, 0, 0),
        )
        # define right track, track 2
        draw.rectangle(
            [
                int(width / 2 + sep / 2),
                int(hsub),
                int(width / 2 + sep / 2 + track2),
                int(hsub + th),
            ],
            fill=(0, 0, 255),
        )

        # define right GND
        draw.rectangle(
            [
                int(width / 2 + sep / 2 + track2 + gap),
                int(hsub),
                int(width),
                int(hsub + th),
            ],
            fill=(0, 255, 0),
        )
        # Save the image as a 24-bit BMP file
        image = ImageOps.flip(image)
        image.save(f"temp/output_{ti}_{si}.bmp", "BMP")

        # print('simulating ..')

        result = subprocess.run(
            f"atlc -d c8c8c8={er} temp/output_{ti}_{si}.bmp",
            shell=True,
            capture_output=True,
            text=True,
        )
        pattern = r"(\w+)=\s*([\d\.\-]+)"
        matches = re.findall(pattern, result.stdout)

        # Convert matches into a dictionary
        data = dict(matches)

        # Optionally, add any additional data you may need (e.g., filename or version)
        data["filename"] = f"temp/output_{ti}_{si}.bmp"
        data["version"] = "4.6.1"
        data["track1"] = track1
        data["track2"] = track2
        data["sep"] = sep
        data["gap"] = gap

        datalist.append(data)

# Create a pandas DataFrame (you can add more rows if needed)
df = pd.DataFrame(datalist)
df.to_csv("temp/edge_coupled_cpw.csv")


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm

X = df["track2"].values
Y = df["sep"].values
Z = df["Zodd"].values

# Create a grid for the contour plot
X_grid, Y_grid = np.meshgrid(np.unique(X), np.unique(Y))

# Z values in a grid shape
Z_grid = np.zeros_like(X_grid)

# Fill Z_grid with values corresponding to X and Y
for i in range(len(X)):
    x_idx = np.where(X_grid[0, :] == X[i])[0][0]
    y_idx = np.where(Y_grid[:, 0] == Y[i])[0][0]
    Z_grid[y_idx, x_idx] = Z[i]

# Step 5: Plot the contour
plt.figure(figsize=(8, 6))
contour = plt.contourf(X_grid, Y_grid, Z_grid, cmap=cm.viridis)
plt.colorbar(contour)
plt.xlabel("track2")
plt.ylabel("sep")
plt.title("Contour plot of Zeven")
plt.show()
