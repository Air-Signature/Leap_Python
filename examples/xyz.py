import matplotlib.pyplot as plt
import numpy as np

def make_dashedLines(x,y,z,ax):
    for i in range(0, len(x)):
        x_val, y_val, z_val = x[i],y[i],z[i]
        ax.plot([0,x_val],[y_val,y_val],zs=[0,0], linestyle="dashed",color="black")
        ax.plot([x_val,x_val],[0,y_val],zs=[0,0], linestyle="dashed",color="black")
        ax.plot([x_val,x_val],[y_val,y_val],zs=[0,z_val], linestyle="dashed",color="black")

fig = plt.figure()

ax = fig.add_subplot(111, projection='3d')

# Make a 3D quiver plot
x, y, z = np.array([[-2,0,0],[0,-2,0],[0,0,-2]])
u, v, w = np.array([[4,0,0],[0,4,0],[0,0,4]])
ax.quiver(x,y,z,u,v,w,arrow_length_ratio=0.1, color="black")
ax.grid(False)
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

ax.set_xlim(0,2)
ax.set_ylim(0,2)
ax.set_zlim(0,2)

plt.show()