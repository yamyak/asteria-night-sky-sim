import csv
# from Star import Star
import numpy as np


class StarChart:

    def __init__(self):
        self.star_list = []

    def load_file(self, file_path):
        csv_file = open(file_path, 'r')
        csv_data = csv.DictReader(csv_file)

        for row in csv_data:
            # star = Star(float(row['x']), float(row['y']), float(row['z']))
            star = np.matrix([[float(row['x'])], [float(row['y'])], [float(row['z'])]])
            self.star_list.append(star)

        csv_file.close()

    def load_data(self, input_data):
        for element in input_data:
            # star = Star(element[0], element[1], element[2])
            star = np.matrix([[element[0]], [element[1]], [element[2]]])
            self.star_list.append(star)

    def find_nearby_stars(self, center, node):
        # direction = (node[0]-center[0], node[1]-center[1], node[2]-center[2])
        return self.star_list
