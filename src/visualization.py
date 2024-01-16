from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import matplotlib.pyplot as plt
import numpy as np
def visualize_pyramid(settings):
    cavity_center = settings['cavity_center']
    cavity_radius = settings['cavity_radius']
    base_length = settings['pyramid_base_length']
    height = settings['pyramid_height']
    queen_chamber_center = settings['queen_chamber_center']
    queen_chamber_width = settings['queen_chamber_width']
    grand_gallery_height = settings['grand_gallery_height']
    grand_gallery_length = settings['grand_gallery_length']
    grand_gallery_width_bottom = settings['grand_gallery_width_bottom']
    grand_gallery_width_top = settings['grand_gallery_width_top']
    grand_gallery_base_center = settings['grand_gallery_base_center'] 
    grand_gallery_incline = settings['grand_gallery_incline']
    king_chamber_center = settings['king_chamber_center']
    king_chamber_width = settings['king_chamber_width']
    king_chamber_height = settings['king_chamber_height']
    detector_position_1 = settings['detector_position_1']
    detector_position_2 = settings['detector_position_2']
    detector_base_vectors_1 = settings['detector_base_vectors_1']
    detector_base_vectors_2 = settings['detector_base_vectors_2']
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111, projection='3d')

    # Define pyramid vertices
    pyramid_vertices = np.array([
        [0, 0, 0],
        [base_length, 0, 0],
        [base_length, base_length, 0],
        [0, base_length, 0],
        [base_length / 2, base_length / 2, height]
    ])
    # Define pyramid faces
    pyramid_faces = [(pyramid_vertices[4], pyramid_vertices[i], pyramid_vertices[(i + 1) % 4]) for i in range(4)]
    queen_chamber_vertices = np.array([
        [queen_chamber_center[0], queen_chamber_center[1], queen_chamber_center[2]],
        [queen_chamber_center[0], queen_chamber_center[1] + queen_chamber_width/2, queen_chamber_center[2]],
        [queen_chamber_center[0] + queen_chamber_width/2, queen_chamber_center[1] + queen_chamber_width/2, queen_chamber_center[2]],
        [queen_chamber_center[0] + queen_chamber_width/2, queen_chamber_center[1], queen_chamber_center[2]],
        [queen_chamber_center[0], queen_chamber_center[1], queen_chamber_center[2] + queen_chamber_width/2],
        [queen_chamber_center[0], queen_chamber_center[1] + queen_chamber_width/2, queen_chamber_center[2] + queen_chamber_width/2],
        [queen_chamber_center[0] + queen_chamber_width/2, queen_chamber_center[1] + queen_chamber_width/2, queen_chamber_center[2] + queen_chamber_width/2],
        [queen_chamber_center[0] + queen_chamber_width/2, queen_chamber_center[1], queen_chamber_center[2] + queen_chamber_width/2]
    ])
    queen_chamber_faces = [
        [queen_chamber_vertices[0], queen_chamber_vertices[1], queen_chamber_vertices[2], queen_chamber_vertices[3]],  
        [queen_chamber_vertices[4], queen_chamber_vertices[5], queen_chamber_vertices[6], queen_chamber_vertices[7]],  
        [queen_chamber_vertices[0], queen_chamber_vertices[1], queen_chamber_vertices[5], queen_chamber_vertices[4]],  
        [queen_chamber_vertices[1], queen_chamber_vertices[2], queen_chamber_vertices[6], queen_chamber_vertices[5]],  
        [queen_chamber_vertices[2], queen_chamber_vertices[3], queen_chamber_vertices[7], queen_chamber_vertices[6]],  
        [queen_chamber_vertices[3], queen_chamber_vertices[0], queen_chamber_vertices[4], queen_chamber_vertices[7]]   
    ]

    incline_rise = np.tan(np.radians(grand_gallery_incline)) * grand_gallery_length

    grand_gallery_vertices = np.array([
        [grand_gallery_base_center[0] - grand_gallery_width_bottom / 2, grand_gallery_base_center[1], grand_gallery_base_center[2]],
        [grand_gallery_base_center[0] + grand_gallery_width_bottom / 2, grand_gallery_base_center[1], grand_gallery_base_center[2]],
        [grand_gallery_base_center[0] + grand_gallery_width_top / 2, grand_gallery_base_center[1] + grand_gallery_length, grand_gallery_base_center[2] + incline_rise],
        [grand_gallery_base_center[0] - grand_gallery_width_top / 2, grand_gallery_base_center[1] + grand_gallery_length, grand_gallery_base_center[2] + incline_rise],
        [grand_gallery_base_center[0] - grand_gallery_width_bottom / 2, grand_gallery_base_center[1], grand_gallery_base_center[2] + grand_gallery_height],
        [grand_gallery_base_center[0] + grand_gallery_width_bottom / 2, grand_gallery_base_center[1], grand_gallery_base_center[2] + grand_gallery_height],
        [grand_gallery_base_center[0] + grand_gallery_width_top / 2, grand_gallery_base_center[1] + grand_gallery_length, grand_gallery_base_center[2] + incline_rise + grand_gallery_height],
        [grand_gallery_base_center[0] - grand_gallery_width_top / 2, grand_gallery_base_center[1] + grand_gallery_length, grand_gallery_base_center[2] + incline_rise + grand_gallery_height]
    ])

    # Define Grand Gallery faces
    grand_gallery_faces = [
        [grand_gallery_vertices[0], grand_gallery_vertices[1], grand_gallery_vertices[5], grand_gallery_vertices[4]],  # Bottom face
        [grand_gallery_vertices[2], grand_gallery_vertices[3], grand_gallery_vertices[7], grand_gallery_vertices[6]],  # Top face
        [grand_gallery_vertices[0], grand_gallery_vertices[3], grand_gallery_vertices[7], grand_gallery_vertices[4]],  # Side face 1
        [grand_gallery_vertices[1], grand_gallery_vertices[2], grand_gallery_vertices[6], grand_gallery_vertices[5]],  # Side face 2
        [grand_gallery_vertices[0], grand_gallery_vertices[1], grand_gallery_vertices[2], grand_gallery_vertices[3]],  # Front face
        [grand_gallery_vertices[4], grand_gallery_vertices[5], grand_gallery_vertices[6], grand_gallery_vertices[7]]   # Back face
    ]
    king_chamber_vertices = np.array([
        [king_chamber_center[0], king_chamber_center[1], king_chamber_center[2]],
        [king_chamber_center[0], king_chamber_center[1] + king_chamber_width/2, king_chamber_center[2]],
        [king_chamber_center[0] + king_chamber_width/2, king_chamber_center[1] + king_chamber_width/2, king_chamber_center[2]],
        [king_chamber_center[0] + king_chamber_width/2, king_chamber_center[1], king_chamber_center[2]],
        [king_chamber_center[0], king_chamber_center[1], king_chamber_center[2] + king_chamber_height/2],
        [king_chamber_center[0], king_chamber_center[1] + king_chamber_width/2, king_chamber_center[2] + king_chamber_height/2],
        [king_chamber_center[0] + king_chamber_width/2, king_chamber_center[1] + king_chamber_width/2, king_chamber_center[2] + king_chamber_height/2],
        [king_chamber_center[0] + king_chamber_width/2, king_chamber_center[1], king_chamber_center[2] + king_chamber_height/2]
    ]) 
    king_chamber_faces = [
        [king_chamber_vertices[0], king_chamber_vertices[1], king_chamber_vertices[2], king_chamber_vertices[3]],  
        [king_chamber_vertices[4], king_chamber_vertices[5], king_chamber_vertices[6], king_chamber_vertices[7]],  
        [king_chamber_vertices[0], king_chamber_vertices[1], king_chamber_vertices[5], king_chamber_vertices[4]],  
        [king_chamber_vertices[1], king_chamber_vertices[2], king_chamber_vertices[6], king_chamber_vertices[5]],  
        [king_chamber_vertices[2], king_chamber_vertices[3], king_chamber_vertices[7], king_chamber_vertices[6]],  
        [king_chamber_vertices[3], king_chamber_vertices[0], king_chamber_vertices[4], king_chamber_vertices[7]]   
    ]
    pyramid = Poly3DCollection(pyramid_faces, facecolors='blue', linewidths=1, edgecolors='r', alpha=.25)
    #queen_chamber = Poly3DCollection(queen_chamber_faces, facecolors = 'green', linewidths=1, edgecolors = 'b', alpha=.25)
    #grand_gallery = Poly3DCollection(grand_gallery_faces, facecolors='grey', linewidths=1, edgecolors='b', alpha=.25)
    #king_chamber = Poly3DCollection(king_chamber_faces,facecolors = 'green', linewidths=1,edgecolors = 'b',alpha=.25 )
    ax.add_collection3d(pyramid)
    #ax.add_collection3d(queen_chamber)
    #ax.add_collection3d(grand_gallery)
    #ax.add_collection3d(king_chamber)
    # Define and plot the test point
    # test_point = [50, 50, 50]
    # test_lane = [115, 200, 120]
    # test_direction = [0, -1, -1]

    # Plot the starting point of the ray
    # ax.scatter(*test_lane, color='green', s=50)

    # Determine the length of the ray to plot

    # ray_length = 100

    # Calculate the end point of the ray
    # end_point = [test_lane[i] + ray_length * test_direction[i] for i in range(3)]

    # Plot the ray
    # ax.plot([test_lane[0], end_point[0]], [test_lane[1], end_point[1]], [test_lane[2], end_point[2]], color='red')

    #ax.scatter(*test_point, color='green', s=50)  # s is the size of the point

    # Define detector vertices by the data of the article
    detector_vertices_1 = np.array([
        detector_base_vectors_1[0],
        detector_base_vectors_1[1],
        detector_base_vectors_1[2],
        detector_base_vectors_1[3],
        [detector_position_1[0], detector_position_1[1], detector_position_1[2]]
    ])

    #detector_faces_1 = [(detector_vertices_1[4], detector_vertices_1[i], detector_vertices_1[(i + 1) % 4]) for i in range(4)]
    #detector_1 = Poly3DCollection(detector_faces_1, facecolors='blue', linewidths=1, edgecolors='r', alpha=.25)
    #ax.add_collection3d(detector_1)

    # Define detector vertices by the data of the article
    detector_vertices_2 = np.array([
        detector_base_vectors_2[0],
        detector_base_vectors_2[1],
        detector_base_vectors_2[2],
        detector_base_vectors_2[3],
        [detector_position_2[0], detector_position_2[1], detector_position_2[2]]
    ])

    #detector_faces_2 = [(detector_vertices_2[4], detector_vertices_2[i], detector_vertices_2[(i + 1) % 4]) for i in range(4)]
    #detector_2 = Poly3DCollection(detector_faces_2, facecolors='blue', linewidths=1, edgecolors='r', alpha=.25)
    #ax.add_collection3d(detector_2)

    #test_point_1 = [115, 247, 0]
    #test_point_2 = [112, 115, 32]
    #ax.scatter(*test_point_1, color='green', s=50)
    #ax.scatter(*test_point_2, color='green', s=50)
    # Plot the cavity
    u, v = np.mgrid[0:2*np.pi:20j, 0:np.pi:10j]
    x = cavity_center[0] + cavity_radius * np.cos(u) * np.sin(v)
    y = cavity_center[1] + cavity_radius * np.sin(u) * np.sin(v)
    z = cavity_center[2] + cavity_radius * np.cos(v)
    ax.plot_wireframe(x, y, z, color="r")


    ## test
    #t_1 = [100.87951363,  63.81758502,  77.13603754]
    #t_2 = [104.22268028,  75.93553467,  75.32812913]
    #ax.scatter(*t_1, color='green', s=50)
    #ax.scatter(*t_2, color='green', s=50)


    # Set labels and limits
    ax.set_xlabel('X Axis')
    ax.set_ylabel('Y Axis')
    ax.set_zlabel('Z Axis')
    ax.set_title('Pyramid Model')
    ax.set_xlim(0, base_length + 50)
    ax.set_ylim(0, base_length + 50)
    ax.set_zlim(0, height + 50)

    plt.show()

