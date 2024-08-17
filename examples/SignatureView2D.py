import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pandas as pd

FileName = input("Enter File Name ")
csv_file_path = 'Sign/{FileName}.csv'.format(FileName=FileName)

df = pd.read_csv(csv_file_path)
# Assuming df_1 is your DataFrame
x_coords = df['index_x_coor']
y_coords = df['index_y_coor']
z_coords = df['index_z_coor']
targets = df['target']

# Initialize variables to track segment start indices
segment_start = 0

# Create a 3D plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Plot each segment separately
for i in range(1, len(targets)):
    if targets[i] == 0:
        # If target is 0, plot the current segment and move to the next one
        ax.plot(x_coords[segment_start:i], y_coords[segment_start:i], z_coords[segment_start:i], '-', color='b', label=f'Segment {i - segment_start}')
        segment_start = i + 1

# Plot the last segment (if any)
if segment_start < len(targets):
    ax.plot(x_coords[segment_start:], y_coords[segment_start:], z_coords[segment_start:], '-', color='b', label=f'Last Segment')

# Customize plot labels and title
ax.set_xlabel(' X ')
ax.set_ylabel(' Y ')
ax.set_zlabel(' Z ')
ax.set_title('3D view of annotated signature')

# Show the plot
plt.show()
