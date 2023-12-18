import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Define the 3D line coordinates
x = [1, 4]
y = [2, 5]
z = [3, 6]

# Create a 3D plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Plot the 3D line
ax.plot(x, y, z, color='red', marker='o')

# Set axis labels
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

# Show the plot
plt.show()
