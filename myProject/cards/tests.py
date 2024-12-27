import json

def load_sign_data(json_file):
    with open(json_file, 'r') as file:
        data = json.load(file)
    return data['traffic_signals']
