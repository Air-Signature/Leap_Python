import sys
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from PyQt5.QtWidgets import QApplication, QMainWindow, QSizePolicy, QVBoxLayout, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import pandas as pd
import numpy as np
from datetime import datetime
class RealTime3DPlot(QMainWindow):

    def __init__(self, df,csv_file_path):
        
        super().__init__()
        self.csv_file_path = csv_file_path
        self.df = df
        self.frame_id_list= []
        self.new_df = self.df.copy()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Real-Time 3D Plot')
        self.setGeometry(600, 600, 1800, 1600)

        self.centralWidget = QWidget(self)
        self.setCentralWidget(self.centralWidget)

        self.layout = QVBoxLayout(self.centralWidget)

        self.fig = plt.Figure()
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.scatter = self.ax.scatter(self.df['index_x_coor'], self.df['index_y_coor'], self.df['index_z_coor'], c='r', picker=True)

        # Set the same limits for all axes
        min_limit = min(min(self.df['index_x_coor']), min(self.df['index_y_coor']), min(self.df['index_z_coor']))
        max_limit = max(max(self.df['index_x_coor']), max(self.df['index_y_coor']), max(self.df['index_z_coor']))

        # self.ax.set_xlim([min_limit, max_limit])
        # self.ax.set_ylim([min_limit, max_limit])
        # self.ax.set_zlim([min_limit, max_limit])

        # Optional: Set the box aspect ratio to make the intervals equal
        self.ax.set_aspect('equal')

        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.ax.set_zlabel('Z')

        self.ax.view_init(elev=90, azim=-90)

        self.canvas = FigureCanvas(self.fig)
        self.canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.layout.addWidget(self.canvas)

        self.canvas.mpl_connect('pick_event', self.on_pick)

        zoom_func = self.zoom_factory(self.ax)
        self.canvas.mpl_connect('scroll_event', zoom_func)

        self.show()

    def on_pick(self, event):
        ind = list(set(event.ind))  # Convert to set to eliminate duplicates
        # print(event.mouseevent.xdata, event.mouseevent.ydata)
        # print(ind)

        
        for i in ind:
            frame_id = self.df.at[self.df.index[i], 'frame_id']
            # print(frame_id)
            self.frame_id_list.append(frame_id)
            self.df.drop(self.df.index[i], inplace=True)

        # Update the scatter plot
        self.scatter._offsets3d = (self.df['index_x_coor'], self.df['index_y_coor'], self.df['index_z_coor'])
        self.canvas.draw()



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

    def save_dataframe_to_csv(self):

        #update coordinates target
        for fid in self.frame_id_list:
            # print(fid)
            try:
                self.new_df.at[self.new_df.loc[self.new_df['frame_id'] == fid].index[0], 'target'] = 0


            except IndexError:
                pass
        now = datetime.now()
        date_time = now.strftime("%m.%d.%Y_%H.%M.%S")
        # csv_file_name = 'Signatures/{FileName}.csv'.format(FileName = self.csv_file_path+"_"+date_time)
        csv_file_name = 'Signatures/updated_{FileName}.csv'.format(FileName = self.csv_file_path)
        
        self.new_df.to_csv(csv_file_name, index=False)

def main():
    FileName = input("Enter File Name : ")
    csv_file_path = 'Signatures/shiveswaran/{FileName}.csv'.format(FileName = FileName)
    app = QApplication(sys.argv)
    df = pd.read_csv(csv_file_path)
    df = df.loc[df['target'] != 0]
    mainWindow = RealTime3DPlot(df,FileName)

    # Connect the save_dataframe_to_csv method to the application's aboutToQuit signal
    app.aboutToQuit.connect(mainWindow.save_dataframe_to_csv)

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
