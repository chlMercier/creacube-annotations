import matplotlib.pyplot as plt
import matplotlib.patches as patches
import pandas as pa
import numpy as np

# Function to create a rectangle from the given points
def create_rectangle(x1, y1, x2, y2):
    return patches.Rectangle((x1, y1), x2 - x1, y2 - y1, linewidth=1, edgecolor='r', facecolor='none')

# Function to calculate the center of a rectangle
def center_of_rectangle(x1, y1, x2, y2):
    return (x1 + (x2 - x1) / 2, y1 + (y2 - y1) / 2)

# Function to check if two rectangles are approximately connected
def rectangles_connected(center1, center2, tolerance=50):
    distance = np.sqrt((center1[0] - center2[0])**2 + (center1[1] - center2[1])**2)
    return distance < tolerance

# Load the data
data = pa.read_csv("in-out_examples/p359/p359.csv", sep=',', skiprows=range(0, 6), header=6)

cube_blanc_coords = data.iloc[:, 3:7]

cube_rouge_coords = data.iloc[:, 11:15]

cube_bleu_coords = data.iloc[:, 19:23]

cube_noir_coords = data.iloc[:, 27:31]

grouped_data = data.groupby(data.columns[0])

fig, ax = plt.subplots()

# Iterate over each group (timestamp)
for name, group in grouped_data:
    centers = {}
    # Calculate centers for each type of cube if not NaN
    if not group.iloc[:, 3:7].isnull().any(axis=1).all():
        centers['cube_blanc'] = group.iloc[:, 3:7].apply(lambda row: center_of_rectangle(*row), axis=1)
    if not group.iloc[:, 11:15].isnull().any(axis=1).all():
        centers['cube_rouge'] = group.iloc[:, 11:15].apply(lambda row: center_of_rectangle(*row), axis=1)
    if not group.iloc[:, 19:23].isnull().any(axis=1).all():
        centers['cube_bleu'] = group.iloc[:, 19:23].apply(lambda row: center_of_rectangle(*row), axis=1)
    if not group.iloc[:, 27:31].isnull().any(axis=1).all():
        centers['cube_noir'] = group.iloc[:, 27:31].apply(lambda row: center_of_rectangle(*row), axis=1)

    # Check connectivity within the timestamp
    for key1, centers1 in centers.items():
        for key2, centers2 in centers.items():
            if key1 != key2:
                for center1 in centers1:
                    for center2 in centers2:
                        if rectangles_connected(center1, center2):
                            print(f"Timestamp {name}: {key1} and {key2} are approximately connected.")