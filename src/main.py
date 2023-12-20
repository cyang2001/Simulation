import pyramid_model
import os
import json



base_dir = os.path.dirname(os.path.abspath(__file__))

settings_path = os.path.join(base_dir, '..', 'config', 'settings.json')


with open(settings_path, 'r') as settings_file:
    settings = json.load(settings_file)  


pyramid_model.plot_pyramid_model(settings=settings)

