import cv2

# Open the webcam (change the index if you have multiple cameras)
cap = cv2.VideoCapture(0)

while True:
    # Read a frame from the webcam
    ret, frame = cap.read()

    # Define the rectangle parameters (x, y, width, height)
    x, y, w, h = 75, 50, 500, 250

    # Draw the rectangle on the frame
    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    # Display the frame
    cv2.imshow('Webcam with Rectangle', frame)

    # Break the loop if 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close the OpenCV window
cap.release()
cv2.destroyAllWindows()
