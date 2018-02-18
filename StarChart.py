import csv
# from Star import Star
import numpy as np


class StarChart:

    def __init__(self):
        """
        Constructor
        """
        self.star_list = []

    def load_file(self, file_path):
        """
        Opens the star data file, reads in the data, and populates the star list
        :param file_path: path to the star data csv
        """
        # open the csv file
        csv_file = open(file_path, 'r')
        csv_data = csv.DictReader(csv_file)

        # create the star list
        for row in csv_data:
            star = np.matrix([[float(row['x'])], [float(row['y'])], [float(row['z'])]])
            self.star_list.append(star)

        # close the csv file
        csv_file.close()

    def load_data(self, input_data):
        """
        Populates the star list with input data
        :param input_data: input star data
        """
        # create the star list
        for element in input_data:
            star = np.matrix([[element[0]], [element[1]], [element[2]]])
            self.star_list.append(star)

    def find_nearby_stars(self, center, node):
        """
        Find all stars that could potentially be visible in viewing plane
        :param center: focus point location
        :param node: viewing plane center location
        :return: list of stars that might be visible in viewing plane
        """
        # direction = (node[0]-center[0], node[1]-center[1], node[2]-center[2])
        return self.star_list
