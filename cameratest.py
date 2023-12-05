import cv2
import time  # Import the time module

pathImage = r"D:\OMR project\Data\1002.jpeg"  # Provide the path to your image file
cap = cv2.VideoCapture(0)
# Initialize the webcam capture if webCamFeed is True
heightImg = 300
widthImg  = 500

widthImg, heightImg = 640, 480  # Set your desired image dimensions

while True:
    # Check if capturing was successful
    if not cap.isOpened():
        img = cv2.imread(pathImage)
    else:
        img = cap.read()
    # Preprocess the image
    img = cv2.resize(img, (widthImg, heightImg)) # RESIZE IMAGE

    # Add your additional image processing code here

    # Display the processed image (optional)
    cv2.imshow("Processed Image", img)

    # Add a delay of 1 second (you can change the delay duration)
    time.sleep(1)

    # Exit the loop when the 'q' key is pressed (you can choose a different exit key)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close any open windows
if cap.isOpened():
    cap.release()
cv2.destroyAllWindows()
