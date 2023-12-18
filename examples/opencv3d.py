
import cv2
import numpy as np

# Create a 3D space with an origin at (0, 0, 0)
origin = np.array([0, 0, 0])

# Define the start and end points of the 3D line
start_point = np.array([1, 2, 3])
end_point = np.array([144, 200,167])

# OpenCV works with 2D images, so we'll project the 3D points onto a 2D plane
# For simplicity, let's use an orthographic projection
projection_matrix = np.array([[1, 0, 0],
                              [0, 1, 0]])

# Project the 3D points onto a 2D plane
start_point_2d = np.dot(projection_matrix, start_point)
end_point_2d = np.dot(projection_matrix, end_point)

# Convert the 2D points to integer coordinates
start_point_2d = tuple(map(int, start_point_2d))
end_point_2d = tuple(map(int, end_point_2d))

# Create a black image
image = np.zeros((500, 500, 3), dtype=np.uint8)

# Draw the line on the image
cv2.line(image, start_point_2d, end_point_2d, (255, 255, 255), 2)

# Display the image
cv2.imshow('3D Line in 2D Space', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
