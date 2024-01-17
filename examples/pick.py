import sys
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from PyQt5.QtWidgets import QApplication, QMainWindow, QSizePolicy, QVBoxLayout, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import pandas as pd

class RealTime3DPlot(QMainWindow):
    def __init__(self, df):
        super().__init__()

        self.df = df

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Real-Time 3D Plot')
        self.setGeometry(100, 100, 800, 600)

        self.centralWidget = QWidget(self)
        self.setCentralWidget(self.centralWidget)

        self.layout = QVBoxLayout(self.centralWidget)

        self.fig = plt.Figure()
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.scatter = self.ax.scatter(self.df['index_x_coor'], self.df['index_y_coor'], self.df['index_z_coor'], c='r', picker=True)


        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.ax.set_zlabel('Z')

        self.ax.view_init(elev=90, azim=-90)

        self.canvas = FigureCanvas(self.fig)
        self.canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.layout.addWidget(self.canvas)

        self.canvas.mpl_connect('pick_event', self.on_pick)

        self.show()

    def on_pick(self, event):
        ind = event.ind

        # Remove selected points from the DataFrame
        self.df.drop(self.df.index[ind], inplace=True)

        # Update the scatter plot
        self.scatter._offsets3d = (self.df['index_x_coor'], self.df['index_y_coor'], self.df['index_z_coor'])


        self.canvas.draw()

def main():
    app = QApplication(sys.argv)
    df = pd.read_csv('../Signatures/Object_Vinojith/1.csv')
    mainWindow = RealTime3DPlot(df)
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
