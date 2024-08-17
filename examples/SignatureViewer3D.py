import sys
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from PyQt5.QtWidgets import QApplication, QMainWindow, QSizePolicy, QVBoxLayout, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import pandas as pd
import numpy as np
from datetime import datetime


class RealTime3DPlot(QMainWindow):

    def __init__(self, df, csv_file_path):
        super().__init__()
        self.csv_file_path = csv_file_path
        self.df = df
        self.frame_id_list = []
        self.new_df = self.df.copy()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Real-Time 3D Plot')
        self.setGeometry(100, 100, 1200, 800)  # Adjusted window size

        self.centralWidget = QWidget(self)
        self.setCentralWidget(self.centralWidget)

        self.layout = QVBoxLayout(self.centralWidget)

        self.fig = plt.Figure(figsize=(10, 8))
        self.ax = self.fig.add_subplot(111, projection='3d')

        x_coords = self.df['index_x_coor']
        y_coords = self.df['index_y_coor']
        z_coords = self.df['index_z_coor']
        targets = self.df['target']

        self.plot = self.ax.plot(x_coords, y_coords, z_coords, marker='o', markersize=4, color='b', linestyle='None')

        self.ax.view_init(elev=30, azim=30)  # Adjusted viewing angle

        # Add legend
        self.ax.legend(['Data points'], loc='upper right', fontsize=10)

        self.canvas = FigureCanvas(self.fig)
        self.canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.layout.addWidget(self.canvas)

        zoom_func = self.zoom_factory(self.ax)
        self.canvas.mpl_connect('scroll_event', zoom_func)

        self.show()

    def zoom_factory(self, ax, base_scale=1.5):
        def zoom_fun(event):
            cur_xlim = ax.get_xlim()
            cur_ylim = ax.get_ylim()
            cur_zlim = ax.get_zlim()
            cur_xrange = (cur_xlim[1] - cur_xlim[0]) * 0.5
            cur_yrange = (cur_ylim[1] - cur_ylim[0]) * 0.5
            cur_zrange = (cur_zlim[1] - cur_zlim[0]) * 0.5
            xdata = event.xdata
            ydata = event.ydata
            if event.button == 'up':
                scale_factor = 1 / base_scale
            elif event.button == 'down':
                scale_factor = base_scale
            else:
                scale_factor = 1

            ax.set_xlim([xdata - cur_xrange * scale_factor, xdata + cur_xrange * scale_factor])
            ax.set_ylim([ydata - cur_yrange * scale_factor, ydata + cur_yrange * scale_factor])
            ax.set_zlim([cur_zlim[0] - cur_zrange * scale_factor, cur_zlim[1] + cur_zrange * scale_factor])

            self.canvas.draw()

        return zoom_fun


def main():
    FileName = input("Enter File Name : ")
    csv_file_path = 'Sign/{FileName}.csv'.format(FileName=FileName)
    app = QApplication(sys.argv)
    df = pd.read_csv(csv_file_path)
    df = df.loc[df['target'] != 0]
    mainWindow = RealTime3DPlot(df, FileName)

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
