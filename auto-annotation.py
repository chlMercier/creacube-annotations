import pandas as pd
import numpy as np
import json
import os

# Load the JSON file containing configurations
with open("configurations.json", "r", encoding="UTF-8") as config:
    CONFIGURATIONS = json.load(config)

OUTPUT_DIR = 'data'
INPUT_DIR = 'in-out_examples\\p359'

# Function to calculate the center of a rectangle
def center_of_rectangle(x1, y1, x2, y2):
    return ((x1 + x2) / 2, (y1 + y2) / 2)

# Functions to check connections along each axis
def connected_x(edge1, edge2, tolerance=10):
    # Check if the rectangles overlap or are within tolerance on the X-axis (back-to-front)
    return abs(edge1[2] - edge2[3]) < tolerance or abs(edge2[2] - edge1[3]) < tolerance

def connected_y(edge1, edge2, tolerance=10):
    # Check if the rectangles overlap or are within tolerance on the Y-axis (left-to-right)
    return abs(edge1[0] - edge2[1]) < tolerance or abs(edge2[0] - edge1[1]) < tolerance

def connected_z(center1, center2, tolerance=50):
    # Check if the distance on the Z-axis (top-to-bottom) is within tolerance
    distance = np.sqrt((center1[0] - center2[0])**2 + (center1[1] - center2[1])**2)
    return distance < tolerance


def process_data(file_path):
    # Load the data
    data = pd.read_csv(file_path, sep=',', skiprows=range(0, 6), header=6, low_memory=False)

    cube_coords = {
        'W': data.iloc[:, 3:7].values,
        'I': data.iloc[:, 11:15].values,
        'B': data.iloc[:, 19:23].values,
        'S': data.iloc[:, 27:31].values,
    }

    timestamps = data.iloc[:, 0]

    # Initialize tracking variables
    last_config = None
    frame_threshold = 2
    missing_frames = 0

    # Iterate over each timestamp
    results = []
    for i, timestamp in enumerate(timestamps):
        centers = {}
        edges = {}

        for cube, coords in cube_coords.items():
            row = coords[i]
            if not np.isnan(row).all():
                x1, y1, x2, y2 = row
                centers[cube] = center_of_rectangle(x1, y1, x2, y2)
                edges[cube] = (x1, x2, y1, y2)  # (left, right, top, bottom)

        connections = []
        connection_axes = {cube: {'x': False, 'y': False, 'z': False} for cube in centers.keys()}

        cubes = list(centers.keys())
        for j in range(len(cubes)):
            for k in range(j + 1, len(cubes)):
                c1, c2 = cubes[j], cubes[k]
                center1, center2 = centers[c1], centers[c2]
                edge1, edge2 = edges[c1], edges[c2]

                if not connection_axes[c1]['x'] and not connection_axes[c2]['x'] and connected_x(edge1, edge2):
                    connections.append(f"{c1[0].upper()}x{c2[0].upper()}")
                    connection_axes[c1]['x'] = connection_axes[c2]['x'] = True
                elif not connection_axes[c1]['y'] and not connection_axes[c2]['y'] and connected_y(edge1, edge2):
                    connections.append(f"{c1[0].upper()}y{c2[0].upper()}")
                    connection_axes[c1]['y'] = connection_axes[c2]['y'] = True
                elif not connection_axes[c1]['z'] and not connection_axes[c2]['z'] and connected_z(center1, center2):
                    connections.append(f"{c1[0].upper()}z{c2[0].upper()}")
                    connection_axes[c1]['z'] = connection_axes[c2]['z'] = True

                # Break out of the loop if we already have 3 connections
                if len(connections) >= 3:
                    break
            if len(connections) >= 3:
                break

        # Match with a configuration that contains all connections
        matched_config = next((config_key for config_key, config_vals in CONFIGURATIONS.items() if len(connections) == 3 and set(connections).issubset(set(config_vals.keys()))), None)

        # Convert timestamp to seconds
        timestamp_seconds = timestamp // 60

        # Only add new configurations or reappearances
        if matched_config != last_config:
            missing_frames += 1

            if matched_config or (missing_frames > frame_threshold and last_config and matched_config):
                results.append({"time": timestamp_seconds, "tclicks": [matched_config]})
                last_config = matched_config
                missing_frames = 0

    return results

def process_csv_file(csv_file):
    results = process_data(csv_file)

    # Determine the name of the output JSON file
    base_name = os.path.splitext(os.path.basename(csv_file))[0]
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_file = os.path.join(OUTPUT_DIR, f'{base_name}.json')

    # Write the JSON data to the output file, overwriting if necessary
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=4)
    
    print(f'Processed {csv_file} into {output_file}')

def process_directory(directory):
    # Iterate over each CSV file in the directory
    for file in os.listdir(directory):
        if file.endswith('.csv'):
            process_csv_file(os.path.join(directory, file))

def main(path):
    # Check if the path is a file or directory
    if os.path.isfile(path) and path.endswith('.csv'):
        process_csv_file(path)
    elif os.path.isdir(path):
        process_directory(path)
    else:
        print("Invalid path. Please provide a path to a CSV file or a directory containing CSV files.")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        main(INPUT_DIR)
    else:
        main(sys.argv[1])