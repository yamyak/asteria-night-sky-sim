import numpy as np
import csv


class StarChart:

    def __init__(self):
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

    def get_data(self):
        """
        Return the star list
        """
        return self.star_list
