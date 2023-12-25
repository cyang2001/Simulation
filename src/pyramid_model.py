from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import matplotlib.pyplot as plt
import numpy as np

class Pyramid:
  def __init__(self, base_length, height):
    """
    Initialize the Pyramid class.

    Parameters:
    base_length (float): The length of the base of the pyramid.
    height (float): The height of the pyramid.

    Returns:
    None
    """
    self.base_length = base_length
    self.height = height
    self.center = np.array([base_length / 2, base_length / 2, 0])  

  def is_inside(self, point):
    """
    Check if a given point is inside the pyramid.

    Parameters:
    point (np.array): The coordinates of the point to check.

    Returns:
    bool: True if the point is inside the pyramid, False otherwise.
    """
    apex = np.array([self.base_length / 2, self.base_length / 2, self.height])
    base_corners = [
        np.array([0, 0, 0]),
        np.array([self.base_length, 0, 0]),
        np.array([self.base_length, self.base_length, 0]),
        np.array([0, self.base_length, 0])
    ]

    # Calculate the volume of the pyramid
    pyramid_volume = self.base_length ** 2 * self.height / 3

    # Calculate the volume of the tetrahedra formed by the point and the faces of the pyramid
    total_volume = 0
    for i in range(4):
        tetra_volume = np.abs(np.dot(np.cross(base_corners[i] - point, base_corners[(i + 1) % 4] - point), apex - point)) / 6
        total_volume += tetra_volume

    # Calculate the volume of the tetrahedra formed by the point and the base
    base_triangle_1 = [base_corners[0], base_corners[1], base_corners[2]]
    base_triangle_2 = [base_corners[2], base_corners[3], base_corners[0]]
    for base_triangle in [base_triangle_1, base_triangle_2]:
        base_tetra_volume = np.abs(np.dot(np.cross(base_triangle[1] - point, base_triangle[2] - point), base_triangle[0] - point)) / 6
        total_volume += base_tetra_volume

    # The point is inside if the total volume of tetrahedra is approximately equal to the pyramid volume
    return np.isclose(total_volume, pyramid_volume, atol=1e-5)



  def path_length(self, position, direction):
      """
      Calculate the path length of a ray inside the pyramid.

      Parameters:
      position (np.array): The starting position of the ray.
      direction (np.array): The direction of the ray.

      Returns:
      float: The path length of the ray inside the pyramid.
      """
      intersection_distances = []
      for face in self._pyramid_faces():
          distance = self._intersect_face(face, position, direction)
          if distance is not None:
              intersection_distances.append(distance)

      if len(intersection_distances) >= 2:
          # Get the smallest and largest distances which represent the entry and exit points
          entry_distance = min(intersection_distances)
          exit_distance = max(intersection_distances)
          return exit_distance - entry_distance
      else:
          return 0  # Handle cases with fewer than 2 intersections appropriately



  def _pyramid_faces(self):
    """
    Get the faces of the pyramid.

    Returns:
    list: A list of tuples representing the faces of the pyramid.
    Each tuple contains three points representing a face.
    """
    apex = np.array([self.base_length / 2, self.base_length / 2, self.height])
    base_corners = [
      np.array([0, 0, 0]),
      np.array([self.base_length, 0, 0]),
      np.array([self.base_length, self.base_length, 0]),
      np.array([0, self.base_length, 0])
    ]
    base_faces = [(base_corners[0], base_corners[1], base_corners[2]),
                  (base_corners[0], base_corners[2], base_corners[3])]
    return [(apex, base_corners[i], base_corners[(i + 1) % 4]) for i in range(4)] + base_faces
  

  def _intersect_face(self, face, position, direction):
      # Extract the points of the face (triangle)
      apex, corner1, corner2 = face

      # Compute the normal vector to the face
      normal = np.cross(corner2 - corner1, apex - corner1)
      normal = normal / np.linalg.norm(normal)  # Normalize the normal vector

      # Check if the ray is parallel to the face
      dot_product = np.dot(normal, direction)
      if np.isclose(dot_product, 0, atol=1e-6):
          return None  # Ray is parallel, no intersection

      # Calculate the intersection parameter
      t = np.dot(normal, corner1 - position) / dot_product
      if t < 0:
          return None  # Intersection behind the ray's start, ignore

      # Calculate the intersection point
      intersect_point = position + [t * d for d in direction]

      # Check if the intersection point is within the triangle
      if self._point_in_triangle(intersect_point, apex, corner1, corner2):
          return t

      return None




  def _point_in_triangle(self, point, vertex1, vertex2, vertex3):
    """
    Check if a point is inside a triangle.

    Parameters:
    point (list): The coordinates of the point to check.
    vertex1 (list): The coordinates of the first vertex of the triangle.
    vertex2 (list): The coordinates of the second vertex of the triangle.
    vertex3 (list): The coordinates of the third vertex of the triangle.

    Returns:
    bool: True if the point is inside the triangle, False otherwise.
    """
    def sign(p1, p2, p3):
      return (p1[0] - p3[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p3[1])

    d1 = sign(point, vertex1, vertex2)
    d2 = sign(point, vertex2, vertex3)
    d3 = sign(point, vertex3, vertex1)

    has_neg = (d1 < 0) or (d2 < 0) or (d3 < 0)
    has_pos = (d1 > 0) or (d2 > 0) or (d3 > 0)

    return not (has_neg and has_pos)


class Cavity:
  def __init__(self, cavity_center, cavity_radius):
    """
    Initialize the cavity class.

    Parameters:
    cavity_center (list): The coordinates of the cavity center.
    cavity_radius (float): The radius of the cavity.

    Returns:
    None
    """
    self.cavity_center = cavity_center
    self.cavity_radius = cavity_radius
  def does_ray_intersect(self, position, direction):
    """
    Check if a ray intersects with the cavity.

    Parameters:
    position (list): The starting position of the ray.
    direction (list): The direction of the ray.

    Returns:
    bool: True if the ray intersects with the cavity, False otherwise.
    """
    # sphere equation: (x - x0)^2 + (y - y0)^2 + (z - z0)^2 = r^2
    # ray equation: x = x0 + at, y = y0 + bt, z = z0 + ct
    # solve for t: (a^2 + b^2 + c^2)t^2 + 2(a(x0 - x) + b(y0 - y) + c(z0 - z))t + (x0^2 + y0^2 + z0^2 - r^2) = 0
    a, b, c = direction
    x0, y0, z0 = position
    A = a ** 2 + b ** 2 + c ** 2
    B = 2 * (a * (x0 - self.cavity_center[0]) + b * (y0 - self.cavity_center[1]) + c * (z0 - self.cavity_center[2]))
    C = (x0 - self.cavity_center[0]) ** 2 + (y0 - self.cavity_center[1]) ** 2 + (z0 - self.cavity_center[2]) ** 2 - self.cavity_radius ** 2
    discriminant = B ** 2 - 4 * A * C
    if discriminant < 0:
      return False
    t1 = (-B + np.sqrt(discriminant)) / (2 * A)
    t2 = (-B - np.sqrt(discriminant)) / (2 * A)
    if t1 < 0 and t2 < 0:
      return False
    return True

def initialize_pyramid_and_cavity(settings, to_file=None):
  """
  Args:
    settings (dict): A dictionary containing the settings for the pyramid model.
      - 'cavity_center' (list): The coordinates of the cavity center.
      - 'cavity_radius' (float): The radius of the cavity.
      - 'base_length' (float): The length of the base of the pyramid.
      - 'height' (float): The height of the pyramid.
    to_file (str, optional): The file path to save the plot. Defaults to None.

  Returns:
    pyramid, cavity: The pyramid and cavity objects.
  """
  cavity_center = settings['cavity_center'] 
  cavity_radius = settings['cavity_radius']
  base_length = settings['base_length']
  height = settings['height']
  
  pyramid = Pyramid(base_length, height)
  cavity = Cavity(cavity_center, cavity_radius)
  return pyramid, cavity
