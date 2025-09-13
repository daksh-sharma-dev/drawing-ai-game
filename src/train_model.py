import os
from PIL import Image
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import joblib

image_size = (28,28)
labels = ['circle', 'square', 'triangle']

def convert_images():
    X = []
    y = []
    for label in labels:
        folder = os.path.join('data', label)
        for filename in os.listdir(folder):                                 # Iterate over images in circle, square and traingle folders
            filepath = os.path.join(folder, filename)
            with Image.open(filepath).convert('L') as img:                  # Convert the images to greyscale
                img = img.resize(image_size)                                      # Decrease the size
                arr = np.array(img).flatten() / 255.0                       # Create a 1D array of each pixel, stored as a float from 0 (black) to 1 (white)
            #print(arr.shape)
            X.append(arr)
            y.append(label)
    X = np.array(X)                                                         # Convert to numpy arrays as these are more efficient
    y = np.array(y)
    return X, y

def train(X, y):
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, train_size=0.8, random_state=1, stratify=y)    # Split the data: 20% for testing and 80% for training.
    print(f'Train / Test split: {len(X_train)} / {len(X_test)} samples')    # stratify=y ensures an equal proportion of each label is used in both training and testing.

    model = KNeighborsClassifier(n_neighbors=3)                             # The 3 nearest neighbours are used to predict the value.
    model.fit(X_train, y_train)                                             # Model is trained with the training data.

    predictions = model.predict(X_test)

    accuracy = accuracy_score(y_test, predictions)                          # Get performance data here.
    print(f'Accuracy: {accuracy}')

    print('Classification Report')
    print(classification_report(y_test, predictions))

    print('Confusion matrix')
    print(confusion_matrix(y_test, predictions))

    joblib.dump(model, os.path.join('models', 'knn_model.pkl'))       # Save the model
    print(f'Model saved.')

    return model

X, y = convert_images()
train(X, y)