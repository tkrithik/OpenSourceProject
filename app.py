import cv2 # Import OpenCV library
from vision import Vision # Import Vision class from 'vision.py' module
import time

vision = Vision() # Create an instance of the Vision class
# Initialize the camera
cap = cv2.VideoCapture(0) # Set up the video capture device
fps = 1000 # Set the desired frames per second
delay_time = int(1000/fps) # Calculate the delay time between frames based on the desired fps

while True: # Start a loop that captures frames from the camera until the 'q' key is pressed
    # Capture frame-by-frame
    ret, frame = cap.read() # Read a frame from the video capture device
    time.sleep(4) # Pause for 4 seconds before processing the frame

    if ret: # If a frame was successfully captured
        resize = frame # Store the frame in a variable called 'resize'
        #resize = frame[80:280, 150:330] # Crop the frame to a specific region of interest (ROI) if desired
        cv2.imwrite("frames/frame.jpg", resize) # Save the frame as an image file

        vision.process_image("frames/frame.jpg") # Process the image file using the Vision class
        # Apply additional image processing if desired
        gray = cv2.cvtColor(resize, cv2.COLOR_BGR2GRAY) # Convert the frame to grayscale
        blur = cv2.GaussianBlur(gray, (5, 5), 0) # Apply Gaussian blur to the grayscale frame
        edges = cv2.Canny(blur, 50, 150) # Apply edge detection to the blurred grayscale frame

        # Display the resulting frames
        cv2.imshow('frame', resize) # Show the original frame in a window called 'frame'
        cv2.imshow('edges', edges) # Show the edge detection result in a window called 'edges'

    # Exit loop if 'q' key is pressed
    if cv2.waitKey(delay_time) & 0xFF == ord('q'):
        break

# Release the camera
cap.release() # Release the video capture device
cv2.destroyAllWindows() # Destroy all OpenCV windows
