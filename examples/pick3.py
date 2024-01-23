import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

class RealTime3DPlotter:
    def __init__(self, csv_file_path):
        self.csv_file_path = csv_file_path
        self.load_data()
        self.fig = plt.figure(figsize=(10, 8))
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.graph = self.ax.scatter(self.df['index_x_coor'], self.df['index_y_coor'], self.df['index_z_coor'], c='blue', picker=True)
        self.fig.canvas.mpl_connect('pick_event', self.on_pick)
        self.fig.canvas.mpl_connect('key_press_event', self.on_key)

    def load_data(self):
        self.df = pd.read_csv(self.csv_file_path)
        self.ids = self.df.index

    def on_pick(self, event):
        ind = event.ind[0]
        clicked_id = self.ids[ind]  # Assuming 'ids' is a regular pandas Index

        # Change color of the clicked point
        if hasattr(self.graph, '_facecolor3d'):
            if ind < len(self.graph._facecolor3d):  # Check if the index is within bounds
                self.graph._facecolor3d[ind] = (0, 1, 0, 1)
        else:
            if ind < len(self.graph._facecolors):  # For compatibility with older Matplotlib versions
                self.graph._facecolors[ind] = (0, 1, 0, 1)
                self.graph.set_facecolor(self.graph._facecolors)

        # Set the target to 0 for the clicked point
        self.df.at[ind, 'target'] = 0  # Assuming 'df' is a pandas DataFrame
        self.df.to_csv('updated_data.csv', index=False)  # Save the updated DataFrame to CSV

        # Update the plot
        self.fig.canvas.draw()

    def on_key(self, event):
        if event.key == 'delete':
            # Remove points with target 0
            self.df = self.df[self.df['target'] != 0]

            # Save the updated DataFrame to a new CSV file
            updated_csv_path = 'updated_' + self.csv_file_path
            self.df.to_csv(updated_csv_path, index=False)

            # Reload the updated data
            self.load_data()

            # Update the plot
            self.ax.clear()
            self.graph = self.ax.scatter(self.df['index_x_coor'], self.df['index_y_coor'], self.df['index_z_coor'], c='blue', picker=True)
            self.fig.canvas.draw()

if __name__ == "__main__":
    csv_file_path = 'Signatures/2.csv'
    plotter = RealTime3DPlotter(csv_file_path)
    plt.show()
