import visualization;
import os
import json



base_dir = os.path.dirname(os.path.abspath(__file__))

settings_path = os.path.join(base_dir, '..', 'config', 'settings.json')


with open(settings_path, 'r') as settings_file:
    settings = json.load(settings_file)  


visualization.visualize_pyramid(settings)

