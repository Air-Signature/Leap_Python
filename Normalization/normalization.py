import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def visualize_normalized_vs_non_normalized(file_paths):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5), subplot_kw={'projection': '3d'})

    for file_path in file_paths:
        # Step 1: Read the CSV file
        df = pd.read_csv(file_path)

        # Visualize the non-normalized 3D signature
        ax1.scatter(df['index_x_coor'], df['index_y_coor'], df['index_z_coor'], marker='.', label=f'Non-Normalized - {file_path}')
        ax1.plot(df['index_x_coor'], df['index_y_coor'], df['index_z_coor'],  alpha=0.5)


        # Normalize the signature
        centroid_x = df['index_x_coor'].mean()
        centroid_y = df['index_y_coor'].mean()
        centroid_z = df['index_z_coor'].mean()

        df['index_x_coor'] -= centroid_x
        df['index_y_coor'] -= centroid_y
        df['index_z_coor'] -= centroid_z

        max_distance = max(
            df['index_x_coor'].max() - df['index_x_coor'].min(),
            df['index_y_coor'].max() - df['index_y_coor'].min(),
            df['index_z_coor'].max() - df['index_z_coor'].min()
        )
        scale_factor = 10.0 / max_distance  # Adjust this value based on your preference

        df['index_x_coor'] *= scale_factor
        df['index_y_coor'] *= scale_factor
        df['index_z_coor'] *= scale_factor

        # Visualize the normalized 3D signature
        ax2.scatter(df['index_x_coor'], df['index_y_coor'], df['index_z_coor'], marker='.', label=f'Normalized - {file_path}')
        ax2.plot(df['index_x_coor'], df['index_y_coor'], df['index_z_coor'],  alpha=0.5)

    ax1.set_title('Non-Normalized 3D Signatures')
    ax1.set_xlabel('X')
    ax1.set_ylabel('Y')
    ax1.set_zlabel('Z')
    ax1.view_init(elev=90, azim=-90)
    ax1.legend()

    ax2.set_title('Normalized 3D Signatures')
    ax2.set_xlabel('X')
    ax2.set_ylabel('Y')
    ax2.set_zlabel('Z')
    ax2.view_init(elev=90, azim=-90)
    ax2.legend()

    plt.tight_layout()
    plt.show()

# Example usage with a list of filenames
file_paths_3d_list = ['signatures/2.csv', 'signatures/3.csv','signatures/4.csv','signatures/5.csv']
visualize_normalized_vs_non_normalized(file_paths_3d_list)
