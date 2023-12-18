
import random
from itertools import count
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Create a 3D plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

namafile = 'data3D.csv'
header1 = "x"
header2 = "y"
header3 = "z"

index = count()


def animate(i):
    data = pd.read_csv('output.csv')
    x = data[header1]
    z = data[header2]
    y = data[header3]

    plt.cla()

    ax.plot3D(x, y, z, 'red')


    #plt.legend(loc='upper left')
    #plt.tight_layout()


ani = FuncAnimation(plt.gcf(), animate, interval=10)

plt.tight_layout()
plt.show()
