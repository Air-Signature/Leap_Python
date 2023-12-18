from mpl_toolkits import mplot3d 
import numpy as np 
import matplotlib.pyplot as plt 
import pandas as pd
import matplotlib, time

namafile = 'data3D.csv'
header1 = "x_value"
header2 = "y_value"
header3 = "z_value"

def animate():
    data = pd.read_csv('data3D.csv')
    x = data[header1]
    y = data[header2]
    z = data[header3]

    fig = plt.figure(figsize =(14, 9)) 
    ax = plt.axes(projection ='3d') 

    surf = ax.plot_surface(x, y, z) 
    plt.draw()
    time.sleep(2000)
    surf.remove()
    plt.draw()
    
matplotlib.interactive(True)    
animate() 