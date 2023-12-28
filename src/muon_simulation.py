import numpy as np

class MuonSimulator:
  def __init__(self, settings, pyramid, cavity, detectors):
    """
    Initialize the MuonSimulator class.

    Parameters:
    altitude (float): The altitude at which the muon simulation is performed.
    energy_range (tuple): The range of energy for the generated muons.
    pyramid (Pyramid): The pyramid model.
    cavity (Cavity): The cavity model.
    mean_free_path (float): The mean free path of muons.
    Returns:
    None
    """
    self.altitude = settings['muon_altitude']
    self.energy_range = settings['muon_energy_range']
    self.pyramid = pyramid
    self.cavity = cavity
    self.mean_free_path = settings['muon_mean_free_path']
    self.energy_loss_per_g_cm2 = settings['muon_energy_loss_per_g_cm2']
    self.material_density = settings['pyramid_material_density']
    self.thickness_range = settings['pyramid_material_thickness_range']
    self.radiation_length = settings['muon_radiation_length']
    self.step_size = settings['muon_step_size']
    self.detector_1 = detectors[0]
    self.detector_2 = detectors[1]
  def generate_muons(self, n_muons):
    """
    Generate muons based on the given number.

    Parameters:
    n_muons (int): The number of muons to generate.

    Returns:
    list: A list of tuples containing the position, direction, and energy of each generated muon.
    """
    muons = []
    for _ in range(n_muons):
      position = np.array([115, 115, self.altitude])
      phi = np.random.uniform(0, 2 * np.pi)
      theta = np.arccos(np.random.uniform(-1, 1))
      direction = np.array([np.sin(theta) * np.cos(phi), np.sin(theta) * np.sin(phi), -np.cos(theta)])
      energy = np.random.uniform(self.energy_range[0], self.energy_range[1])
      muons.append((position, direction, energy))
    return muons

  def simulate_muons_trajectory(self, muon):
    """
    Simulates the trajectory of muons.

    Parameters:
    - muons: A tuple containing the position, direction, and energy of the muons.

    Returns:
    - If the muon is outside the pyramid, returns None.
    - If the muon intersects with the cavity, returns a tuple with True, the new position, and the energy.
    - If the muon is absorbed, returns a tuple with False, the new position, and 0 energy.
    - Otherwise, returns a tuple with True, the new position, and the energy.
    """
    position, direction, energy = muon
    if not self.pyramid.is_inside(position):
      return None

    while self.pyramid.is_inside(position):
        position += direction * self.step_size
        length = self.pyramid.path_length(position, direction)
        if np.random.random() < self.absorption_probability(length):
          break
        if self.cavity.is_inside(position, direction):
          energy = self.calculate_energy_loss(energy, 0.00001, self.step_size)
        else:
          energy = self.calculate_energy_loss(energy, self.material_density, self.step_size)
        muon = (position, direction, energy)
        if energy <= 0:
            break  # Muon has lost all its energy and stopped
        if self.detector_1.detect_muon(muon):
          break
        if self.detector_2.detect_muon(muon):
          break

    return muon


  
  def calculate_energy_loss(self, initial_energy, material_density):
      """
      Calculate the energy loss of a muon in the material.

      Parameters:
      initial_energy (float): The initial energy of the muon in MeV.
      material_density (float): The density of the material in g/cm^3.
      thickness (float): The thickness of the material that the muon travels through in cm.

      Returns:
      float: The final energy of the muon after passing through the material.
      """

      energy_loss = self.energy_loss_per_g_cm2 * material_density * np.random.uniform(self.thickness_range[0], self.thickness_range[1]) * 100
      radiation_loss = initial_energy * (1 - np.exp(-np.random.uniform(self.thickness_range[0], self.thickness_range[1]) / (self.radiation_length / material_density)))
      total_loss = energy_loss + radiation_loss
      final_energy = max(initial_energy - total_loss, 0)  # Ensure energy does not go negative
      return final_energy
  def absorption_probability(self, length):
    return 1 - np.exp(-length / self.mean_free_path)