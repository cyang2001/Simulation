
import numpy as np
class MuonDetector:
    def __init__(self, settings, nth_detector):
        self.position = settings[f'detector_position_{nth_detector}']
        self.base_vectors = settings[f'detector_base_vectors_{nth_detector}']
        self.apex = np.array(self.position)
        self.detected_muons = []  
        self.base_area = self.base_vectors[0][0] * self.base_vectors[1][0]
        self.height = self.base_vectors[0][2] - self.position[2]
    def is_inside(self, point):
        """
        Check if a given point is inside the pyramid.

        Parameters:
        point (np.array): The coordinates of the point to check.

        Returns:
        bool: True if the point is inside the pyramid, False otherwise.
        """

        base_corners = [
            np.array(self.base_vectors[0]),
            np.array(self.base_vectors[1]),
            np.array(self.base_vectors[2]),
            np.array(self.base_vectors[3])
        ]

        # Calculate the volume of the pyramid
        pyramid_volume = self.base_area * self.height / 3

        # Calculate the volume of the tetrahedra formed by the point and the faces of the pyramid
        total_volume = 0
        for i in range(4):
            tetra_volume = np.abs(np.dot(np.cross(base_corners[i] - point, base_corners[(i + 1) % 4] - point), self.apex - point)) / 6
            total_volume += tetra_volume

        # Calculate the volume of the tetrahedra formed by the point and the base
        base_triangle_1 = [base_corners[0], base_corners[1], base_corners[2]]
        base_triangle_2 = [base_corners[2], base_corners[3], base_corners[0]]
        for base_triangle in [base_triangle_1, base_triangle_2]:
            base_tetra_volume = np.abs(np.dot(np.cross(base_triangle[1] - point, base_triangle[2] - point), base_triangle[0] - point)) / 6
            total_volume += base_tetra_volume

        # The point is inside if the total volume of tetrahedra is approximately equal to the pyramid volume
        return np.isclose(total_volume, pyramid_volume, atol=1e-5)
    def detect_muon(self, muon):
        """
        Detect a muon and record its information if it passes through the detector.

        Parameters:
        muon (Muon): The muon object to detect.

        Returns:
        bool: True if the muon is detected, False otherwise.
        """
        if self.is_inside(muon.position):
            detection_probability = 0.95  
            if np.random.random() < detection_probability:
                self.detected_muons.append(muon)
                return True
        return False
