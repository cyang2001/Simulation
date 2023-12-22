from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import matplotlib.pyplot as plt
import numpy as np
def visualize_pyramid(settings):

  cavity_center = settings['cavity_center'] 
  cavity_radius = settings['cavity_radius']
  base_length = settings['base_length']
  height = settings['height']
  
  fig = plt.figure(figsize=(10, 10))
  ax = fig.add_subplot(111, projection='3d')

  # Fix the vertices definition here
  pyramid_vertices = np.array([
                [0, 0, 0], 
                [base_length, 0, 0], 
                [base_length, base_length, 0], 
                [0, base_length, 0], 
                [base_length/2, base_length/2, height]])
  
  pyramid_faces = [(pyramid_vertices[4], pyramid_vertices[i], pyramid_vertices[(i + 1) % 4]) for i in range(4)]
  pyramid = Poly3DCollection(pyramid_faces, facecolors='blue', linewidths=1, edgecolors='r', alpha=.25)
  ax.add_collection3d(pyramid)


  u, v = np.mgrid[0:2*np.pi:20j, 0:np.pi:10j]
  x = cavity_center[0] + cavity_radius * np.cos(u) * np.sin(v)
  y = cavity_center[1] + cavity_radius * np.sin(u) * np.sin(v)
  z = cavity_center[2] + cavity_radius * np.cos(v)
  ax.plot_wireframe(x, y, z, color="r")

  ax.set_xlabel('X Axis')
  ax.set_ylabel('Y Axis')
  ax.set_zlabel('Z Axis')
  ax.set_title('Pyramid Model')
  ax.set_xlim(0, base_length)
  ax.set_ylim(0, base_length)
  ax.set_zlim(0, height)
  plt.show()