import matplotlib.pyplot as plt
import pandas as pd

FileName = "Arujan"
csv_file_path = 'Signatures/{FileName}/updated_1.csv'.format(FileName=FileName)

df = pd.read_csv(csv_file_path)
# Assuming df_1 is your DataFrame
x_coords = df['index_x_coor']
y_coords = df['index_y_coor']
z_coords = df['index_z_coor']
targets = df['target']

# Initialize variables to track segment start indices
segment_start = 0

# Plot each segment separately
for i in range(1, len(targets)):
    if targets[i] == 0:
        # If target is 0, plot the current segment and move to the next one
        plt.plot(x_coords[segment_start:i], y_coords[segment_start:i], '-',color='b', label=f'Segment {i - segment_start}')
        segment_start = i + 1

# Plot the last segment (if any)
if segment_start < len(targets):
    plt.plot(x_coords[segment_start:], y_coords[segment_start:], '-',color='b', label=f'Last Segment')

# Customize plot labels and title
plt.xlabel('Index X Coordinate')
plt.ylabel('Index Y Coordinate')
plt.title('Discontinuous Line Plot of Points where Target is 1')

# Show the plot
plt.show()