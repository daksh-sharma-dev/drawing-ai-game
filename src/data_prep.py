import os
import numpy as np
from PIL import Image

def convert_images(image_size, labels):
    X = []
    y = []
    for label in labels:
        folder = os.path.join('data', label)
        for filename in os.listdir(folder):                                 # Iterate over images in circle, square and traingle folders
            filepath = os.path.join(folder, filename)
            with Image.open(filepath).convert('L') as img:                  # Convert the images to greyscale
                img = img.resize(image_size)                                      # Decrease the size
                arr = np.array(img).flatten() / 255.0                       # Create a 1D array of each pixel, stored as a float from 0 (black) to 1 (white)
            X.append(arr)
            y.append(label)
    X = np.array(X)                                                         # Convert to numpy arrays as these are more efficient
    y = np.array(y)
    return X, y