# Import necessary packages
import io
import os.path
import requests
import json
import wikipedia
from pprint import pprint
from google.cloud import vision # Import Google Cloud Vision API client library

# Load food labels from JSON file
f = open('foods.json')
foods = json.load(f)

# Define Vision class with two methods
class Vision:
    def __init__(self): # Constructor method that prints a message when the class is initialized
        print("Initializing Vision Class")

    def process_image(self, frame): # Method that takes an image file and performs label detection on it
        # Create client for Google Cloud Vision API
        client = vision.ImageAnnotatorClient()

        # Load image file into memory
        with io.open(frame, 'rb') as image_file:
            content = image_file.read()

        # Create Google Cloud Vision Image object from image file data
        image = vision.Image(content=content)

        # Perform label detection on image file using Vision API
        response = client.label_detection(image=image)
        labels = response.label_annotations

        # Convert label annotations into a list of lowercase strings
        label_list = []
        for label in labels:
            label_list.append(str(label.description).lower())

        # Check if any of the detected labels match with the food labels in the JSON file
        self.check_label(label_list)

        # Print the list of detected labels
        print(label_list)

    def check_label(self, label_list): # Method that checks if any of the detected labels match with the food labels in the JSON file
        for label in label_list:
            if label in foods:
                print(foods[label]) # Print the corresponding food label from the JSON file if there is a match
