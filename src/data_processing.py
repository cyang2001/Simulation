import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class MuonDataAnalysis:
    def __init__(self, filepath):
        self.filepath = filepath
        self.data = None

    def load_data(self):
        self.data = pd.read_csv(self.filepath)

    def preprocess_data(self):
        pass
    def show(self):
        print(self.data.head())
        self.analyze_energy_loss()
        self.perform_statistical_analysis()
        self.visualize_results()
        self.interpret_results()
    def analyze_energy_loss(self):
        self.data['Total_Energy_Loss'] = self.data.groupby('Muon_ID')['Energy_Loss'].sum()

    def perform_statistical_analysis(self):
        self.mean_energy_loss = self.data['Total_Energy_Loss'].mean()
        self.std_dev_energy_loss = self.data['Total_Energy_Loss'].std()

    def visualize_results(self):
        plt.hist(self.data['Total_Energy_Loss'], bins=50, alpha=0.7)
        plt.xlabel('Total Energy Loss')
        plt.ylabel('Frequency')
        plt.title('Histogram of Total Energy Loss per Muon')
        plt.show()

    def interpret_results(self):
        print(f"Average Energy Loss: {self.mean_energy_loss}")
        print(f"Standard Deviation of Energy Loss: {self.std_dev_energy_loss}")

