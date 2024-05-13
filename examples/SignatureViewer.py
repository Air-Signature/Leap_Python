
import sys
from turtle import xcor
import matplotlib.pyplot as plt
from matplotlib.typing import ColourType
from mpl_toolkits.mplot3d import Axes3D
from PyQt5.QtWidgets import QApplication, QMainWindow, QSizePolicy, QVBoxLayout, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import pandas as pd
import numpy as np
from datetime import datetime

from pyparsing import col


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
    self.setGeometry(1600, 1600, 1800, 1600)

    self.centralWidget = QWidget(self)
    self.setCentralWidget(self.centralWidget)

    self.layout = QVBoxLayout(self.centralWidget)

    self.fig = plt.Figure(figsize=(30, 24))
    self.ax = self.fig.add_subplot(111, projection='3d')

    x_coords = self.df['index_x_coor']
    y_coords = self.df['index_y_coor']
    z_coords = self.df['index_z_coor']
    targets = self.df['target']

    # Initialize variables to track segment start indices

    self.plot = self.ax.plot(x_coords, y_coords, z_coords, linestyle='-', color = 'blue',
                                   alpha=0.5 ,linewidth='0')
    self.plot = self.ax.plot(x_coords, y_coords, z_coords, marker = 'o', ms = 1, mfc = 'b', color = 'blue',
                                   alpha=0.2)
    
    self.plot = self.ax.plot(x_coords, y_coords, z_coords, marker = 'o', ms = 4, mec = 'blue',
                                    alpha=0.5)
    # Optional: Set the box aspect ratio to make the intervals equal
    self.ax.set_aspect('equal')

    self.ax.set_xlabel('X')
    self.ax.set_ylabel('Y')
    self.ax.set_zlabel('Depth')

    self.ax.view_init(elev=120, azim=-120)

    self.canvas = FigureCanvas(self.fig)
    self.canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    self.layout.addWidget(self.canvas)

    zoom_func = self.zoom_factory(self.ax)
    self.canvas.mpl_connect('scroll_event', zoom_func)

    self.show()


  def zoom_factory(self, ax, base_scale=2.):
    def zoom_fun(event):
      cur_xlim = ax.get_xlim()
      cur_ylim = ax.get_ylim()
      cur_xrange = (cur_xlim[1] - cur_xlim[0]) * 0.5
      cur_yrange = (cur_ylim[1] - cur_ylim[0]) * 0.5
      xdata = event.xdata
      ydata = event.ydata
      if event.button == 'up':
        scale_factor = 1 / base_scale
      elif event.button == 'down':
        scale_factor = base_scale
      else:
        scale_factor = 1

      ax.set_xlim([xdata - cur_xrange * scale_factor,
                   xdata + cur_xrange * scale_factor])
      ax.set_ylim([ydata - cur_yrange * scale_factor,
                   ydata + cur_yrange * scale_factor])

      self.canvas.draw()

    return zoom_fun



def main():
  FileName = "chathuva"
  csv_file_path = 'Signatures/{FileName}/5.csv'.format(FileName=FileName)
  app = QApplication(sys.argv)
  df = pd.read_csv(csv_file_path)
  df = df.loc[df['target'] != 0]
  mainWindow = RealTime3DPlot(df, FileName)

  # Connect the save_dataframe_to_csv method to the application's aboutToQuit signal

  sys.exit(app.exec_())


if __name__ == '__main__':
  main()
# test comment added.