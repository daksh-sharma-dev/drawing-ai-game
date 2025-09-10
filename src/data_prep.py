import os
import numpy as np
from PIL import Image
from sklearn.model_selection import train_test_split

image_size = (28,28)
labels = ['circle', 'square', 'triangle']
X, y = [], []

for label in labels:
    folder = os.path.join('../data', label)
    for filename in os.listdir(folder):
        filepath = os.path.join(folder, filename)
        img = Image.open(filepath).convert('L') # grayscaling image
        img = img.resize(image_size)            # resizing image
        arr = np.array(img).flatten() / 255.0   # create a 1D array of each pixel, stored as a float from 0 (black) to 1 (white)
        X.append(arr)
        y.append(label)

X = np.array(X)
y = np.array(y)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, train_size=0.8, random_state=1)
print(f'Training samples: {len(X_train)}, Test Samples: {len(X_test)}')