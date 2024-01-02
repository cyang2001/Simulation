
from multiprocessing import Pool
import numpy as np
import pandas as pd

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
    self.scattering_strength_in_cavity = settings['muon_scattering_strength_in_cavity']
    self.scattering_strength_in_other_material = settings['muon_scattering_strength_in_other_material']
  def random_position_on_side(self, side):

        base_corner1 = np.array([0, 0, 0])
        base_corner2 = np.array([self.pyramid.base_length, 0, 0])
        base_corner3 = np.array([self.pyramid.base_length, self.pyramid.base_length, 0])
        base_corner4 = np.array([0, self.pyramid.base_length, 0])
        apex = np.array([self.pyramid.base_length / 2, self.pyramid.base_length / 2, self.pyramid.height])

        if side == 'side1':
            vertices = [base_corner1, base_corner2, apex]
        elif side == 'side2':
            vertices = [base_corner2, base_corner3, apex]
        elif side == 'side3':
            vertices = [base_corner3, base_corner4, apex]
        else:  # side4
            vertices = [base_corner4, base_corner1, apex]


        r1, r2 = np.random.random(), np.random.random()
        if r1 + r2 > 1:
            r1 = 1 - r1
            r2 = 1 - r2
        position = r1 * vertices[0] + r2 * vertices[1] + (1 - r1 - r2) * vertices[2]
        return position

  def generate_muons(self, n_muons):
      muons = []
      for _ in range(n_muons):
          face_choice = np.random.choice(['side1', 'side2', 'side3', 'side4'])
          position = self.random_position_on_side(face_choice)
          direction = self.random_direction_towards_center(position)

          energy = np.random.uniform(self.energy_range[0], self.energy_range[1])
          muons.append((position, direction, energy))
      return [(i, muon) for i, muon in enumerate(muons)]
  def random_direction_towards_center(self, position):
      center = np.array([self.pyramid.base_length / 2, self.pyramid.base_length / 2, self.pyramid.height / 2])

      direction = center - position

      random_perturbation = np.random.uniform(-1, 1, 3)  
      direction += random_perturbation 

      direction /= np.linalg.norm(direction)  

      return direction
  def simulate_muon_trajectory(self, muon):
        muon_id, (position, direction, energy) = muon
        energy_loss = 0
        is_absorbed = False
        if not self.pyramid.is_inside(position):
            return None

        max_steps = 1500
        dtype = [('position', float, 3), ('direction', float, 3), ('energy', float), ('energy_loss', float), ('is_absorbed', bool)]
        path = np.zeros(max_steps, dtype=dtype) 
        path[0] = (position, direction, energy, energy_loss, is_absorbed)
        step_count = 1

        while self.pyramid.is_inside(position) and step_count < max_steps:
            position += direction * self.step_size
            path[step_count]['position'] = position
            path[step_count]['is_absorbed'] = False
            length = self.pyramid.calculate_length(path[step_count - 1]['position'], position)

            if np.random.random() < self.absorption_probability(length):
                path[step_count]['is_absorbed'] = True
                break
            if self.cavity.is_inside(position):
                energy, energy_loss = self.calculate_energy_loss(energy, [0.00001, 0.0001])
                random_perturbation = np.random.uniform(-self.scattering_strength_in_cavity, self.scattering_strength_in_cavity, direction.shape)
                direction += random_perturbation
                direction /= np.linalg.norm(direction)
            else:
                energy, energy_loss = self.calculate_energy_loss(energy, self.material_density)
                random_perturbation = np.random.uniform(-self.scattering_strength_in_other_material, self.scattering_strength_in_other_material, direction.shape)
                direction += random_perturbation
                direction /= np.linalg.norm(direction)

            path[step_count]['direction'] = direction
            path[step_count]['energy'] = energy
            path[step_count]['energy_loss'] = energy_loss
            if energy <= 0:
                break

            step_count += 1

        return muon_id, path[:step_count]  
  def simulate_muons_parallel(self, n_muons, n_processes=8):
        muons = self.generate_muons(n_muons)
        muon_splits = np.array_split(muons, n_processes)

        with Pool(n_processes) as pool:
            results = pool.map(self.simulate_muon_trajectories_batch, muon_splits)

        all_results = np.concatenate(results)
        self.write_results_to_csv(all_results)

        return all_results

  def simulate_muon_trajectories_batch(self, muon_batch):
      return [self.simulate_muon_trajectory(muon) for muon in muon_batch]

  def write_results_to_csv(self, results):
      
      records = []
      for muon_id, path in results:
          for step in path:
              position, direction, energy, energy_loss, is_absorbed = step['position'], step['direction'], step['energy'], step['energy_loss'], step['is_absorbed']
              records.append([muon_id, position, direction, energy, energy_loss, is_absorbed])

      df = pd.DataFrame(records, columns=['Muon_ID', 'Position', 'Direction', 'Energy', 'Energy_Loss', 'Is_Absorbed'])
      df.to_csv('muon_simulation_results.csv', index=False)
  
  def calculate_energy_loss(self, initial_energy, material_density):
      """
      Calculate the energy loss of a muon in the material.

      Parameters:
      initial_energy (float): The initial energy of the muon in MeV.
      material_density (float): The density of the material in g/cm^3.
      Returns:
      float: The final energy of the muon after passing through the material.
      """

      energy_loss = self.energy_loss_per_g_cm2 * np.random.uniform(material_density[0], material_density[1]) * np.random.uniform(self.thickness_range[0], self.thickness_range[1]) * self.step_size * 100 * 0.001 # Convert to GeV convert to cm
      #radiation_loss = initial_energy * (1 - np.exp(- self.step_size / (self.radiation_length / self.material_density)))
      total_loss = energy_loss #+ radiation_loss
      final_energy = max(initial_energy - total_loss, 0)  # Ensure energy does not go negative
      return final_energy, total_loss
  def absorption_probability(self, length):
    return 1 - np.exp(-length / self.mean_free_path)