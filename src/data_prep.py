import os
import numpy as np
from PIL import Image
from random import randint

def process_images(filepath, image_size):

    # Load image and convert to numpy array.
    with Image.open(filepath).convert('L') as img:                              # Opens the image and converts it to greyscale
        arr = np.array(img)                                                     # Converts to a numpy array

        # Find the pixels that are relevant (i.e. part of the drawing)
        mask = arr < 240                                                        # Creates a boolean array where if a pixel is darker than 240, it is stored as True.

        # Handle empty images
        if not mask.any():                                                      # This means it is an empty image.
            blank_image = np.ones(image_size, dtype=np.float32).flatten() * 0   # Create a blank image.
            return blank_image.flatten()                                        # Convert to 1D array.
        
        # Crop to relevant section
        rows = np.any(mask, axis=1)                                             # Find which rows contain part of the drawing.
        cols = np.any(mask, axis=0)                                             # Find which columns contain part of the drawing.
        rows_with_drawing = np.where(rows)                                     
        first_row = rows_with_drawing[0][0]                                     # Find the first and last rows.
        last_row = rows_with_drawing[0][-1]
        cols_with_drawing = np.where(cols)                                      
        first_col = cols_with_drawing[0][0]                                     # Find the first and last columns.
        last_col = cols_with_drawing[0][-1]

        cropped_image = arr[first_row:last_row+1, first_col:last_col+1]

        # Add padding
        height, width = cropped_image.shape
        padding = 8
        side = max(height, width) + padding
        square = np.ones((side,side), dtype=np.uint8) * 255                     # Create a blank square. uint8 = unsigned 8 bits
        y = (side - height) // 2
        x = (side - width) // 2
        square[y:y+height, x:x+width] = cropped_image

        # Create and resize image
        final_image = Image.fromarray(square)                                   # Creating the 8 bit image.
        final_image = final_image.resize(image_size, Image.LANCZOS)             # Image.LANCZOS is a high quality image fliter.
        final_image_arr = np.array(final_image).astype(np.float32) / 255.0      # Gets the array of pixels, stores as 4 byte floating point numbers, and normalises to between 0 and 1.
        final_image_arr = 1.0 - final_image_arr                                 # Invert. This helps the machine learning model.
        
        # Return as a 1D list.
        return final_image_arr.flatten()

def convert_images(image_size, labels):
    X = []
    y = []
    for label in labels:
        folder = os.path.join('data', label)
        for filename in os.listdir(folder):                                     # Iterate over images in circle, square and traingle folders
            filepath = os.path.join(folder, filename)
            '''with Image.open(filepath).convert('L') as img:                      # Convert the images to greyscale
                img = img.resize(image_size)                                    # Decrease the size
                arr = np.array(img).flatten() / 255.0                           # Create a 1D array of each pixel, stored as a float from 0 (black) to 1 (white)'''
            arr = process_images(filepath, image_size)
            X.append(arr)
            y.append(label)
    X = np.array(X, dtype=np.float32)                                                             # Convert to numpy arrays as these are more efficient
    y = np.array(y)
    return X, y

if __name__ == '__main__':
    X, y = convert_images((28,28), ['circle', 'square', 'triangle'])
    os.makedirs('previews', exist_ok=True)
    for i in range(20):
        n = randint(0, len(X)-1)
        arr = X[n].reshape((28,28))
        arr = (1.0 - arr) * 255.0
        img = Image.fromarray(arr.astype(np.uint8))
        img.save(f'previews/preview_{i}_{y[n]}.png')