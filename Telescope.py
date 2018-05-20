import pygame
import numpy as np
import math


class Telescope:

    def __init__(self, compass):
        """
        Constructor
        :param compass: compass object containing initialization data
        """
        self.width = compass.width
        self.height = compass.height
        self.screen_w = compass.screen_w
        self.screen_h = compass.screen_h

        # initialize pygame screen
        pygame.init()
        self.screen = pygame.display.set_mode((self.screen_w*2, self.screen_h*2))

        self.focus_point = (np.asmatrix(compass.focus_point)).T
        self.plane_point = (np.asmatrix(compass.plane_point)).T

        # convert the cartesian coordinates to polar coordinates
        self.polar = self.convert_to_polar(self.plane_point)

        self.rz = 0
        self.ry = 0
        # create the rotation matrices
        self.create_rotation_matrices()

        self.points = []

        self.chart = None

    def load_chart(self, chart):
        self.chart = chart

    def create_rotation_matrices(self):
        """
        Creates the y and z rotation matrices based off the polar coordinates
        """
        # transform the angles
        phi = -self.polar[1]
        theta = (math.pi / 2) - self.polar[0]

        # create the rotation matrices
        self.rz = np.matrix([[math.cos(phi), -math.sin(phi), 0],
                            [math.sin(phi), math.cos(phi), 0],
                            [0, 0, 1]])
        self.ry = np.matrix([[math.cos(theta), 0, math.sin(theta)],
                            [0, 1, 0],
                            [-math.sin(theta), 0, math.cos(theta)]])

    @staticmethod
    def convert_to_polar(point):
        """
        Converts the cartesian coordinate into polar coordinates
        :param point: matrix of cartesian coordinates x, y, and z
        :return: polar coordinates theta and phi
        """
        n = np.linalg.norm(point)
        norm = point / n

        theta = math.acos(norm.item((2, 0)))
        phi = math.atan2(norm.item((1, 0)), norm.item((0, 0)))

        return theta, phi

    def find_nearby_stars(self):
        """
        Find all stars that could potentially be visible in viewing plane
        :return: list of stars that might be visible in viewing plane
        """
        step_size = math.pi/8

        star_sub_list = []

        star_list = self.chart.get_data()
        for star in star_list:
            star_theta, star_phi = self.convert_to_polar(star)

            if math.fabs(star_phi - self.polar[1]) < step_size and math.fabs(star_theta - self.polar[0]) < step_size:
                star_sub_list.append(star)

        return star_sub_list

    def calculate_view(self):
        """
        Calculate the 2D coordinates on the viewing plane based on the 3D coordinates
        :return: polar coordinates theta and phi
        """
        # create the normal for the viewing panel
        normal = self.plane_point - self.focus_point
        normal = self.rz * normal
        normal = self.ry * normal

        current_stars = self.find_nearby_stars()

        # iterate through list of stars
        for star in current_stars:
            # apply the rotation matrices to the star coordinates
            star_2d = self.rz * star
            star_2d = self.ry * star_2d

            # find the intersection point between the star and the focus point
            star_2d = self.find_intersection(star_2d, normal)

            # if 2D star is within camera plane borders, add to list of stars to draw
            if (0 - self.width) < star_2d.item((1, 0)) < self.width and (0 - self.height) < star_2d.item((2, 0)) < self.height:
                # flip the screen over the vertical axis
                self.points.append((star_2d.item((1, 0)), star_2d.item((2, 0))))

    def find_intersection(self, star, normal):
        """
        Determine the intersection point of the star on the viewing plane
        :param star: 3d point to be transposed onto viewing plane
        :param normal: normal vector to viewing plane
        :return: 3d point on the viewing plane
        """
        d = (normal.T * normal) / ((star - self.focus_point).T * normal)

        return (d.item(0, 0) * (star - self.focus_point)) + self.focus_point

    def change_location(self, focus_point, plane_point):
        """
        Update the focus point and viewing plane locations
        :param focus_point: new focus point
        :param plane_point: new viewing plane center point
        """
        # clear the screen
        self.screen.fill(0, 0, 0)

        self.focus_point = focus_point
        self.plane_point = plane_point

    def update_view(self):
        """
        Draws all 2D star points on the screen
        """
        # iterate through the 2d star point
        for entry in self.points:
            # map the star point onto the screen
            x = entry[0] * self.screen_w / self.width + self.screen_w
            y = self.screen_h*2 - (entry[1] * self.screen_h / self.height + self.screen_h)

            pygame.draw.circle(self.screen, (0, 255, 0), (int(x), int(y)), 1, 0)

        pygame.display.update()

        test = True
