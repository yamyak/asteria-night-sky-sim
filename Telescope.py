import pygame
import numpy as np
import math


class Telescope:

    def __init__(self, width, height, screen_w, screen_h, focus_point, plane_point):
        """
        Constructor
        :param width: 1/2 width of the camera plane
        :param height: 1/2 height of the camera plane
        :param screen_w: 1/2 width of the camera plane in pixels
        :param screen_h: 1/2 height of the camera plane in pixels
        :param focus_point: location that subject eyes are
        :param plane_point: center point of the camera plane
        """
        self.width = width
        self.height = height
        self.screen_w = screen_w
        self.screen_h = screen_h

        # initialize pygame screen
        pygame.init()
        self.screen = pygame.display.set_mode((screen_w*2, screen_h*2))

        self.focus_point = (np.asmatrix(focus_point)).T
        self.plane_point = (np.asmatrix(plane_point)).T

        # convert the cartesian coordinates to polar coordinates
        self.polar = self.convert_to_polar(plane_point)

        self.rz = 0
        self.ry = 0
        # create the rotation matrices
        self.create_rotation_matrices()

        self.points = []

    @staticmethod
    def convert_to_polar(point):
        """
        Converts the cartesian coordinate into polar coordinates
        :param point: matrix of cartesian coordinates x, y, and z
        :return: polar coordinates theta and phi
        """
        theta = math.acos(point[2])
        phi = math.atan2(point[1], point[0])

        return theta, phi

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

    def calculate_view(self, star_list):
        """
        Calculate the 2D coordinates on the viewing plane based on the 3D coordinates
        :param star_list: list of stars to be displayed
        :return: polar coordinates theta and phi
        """
        # create the normal for the viewing panel
        normal = self.plane_point - self.focus_point
        normal = self.rz * normal
        normal = self.ry * normal

        # iterate through list of stars
        for star in star_list:
            # apply the rotation matrices to the star coordinates
            star_2d = self.rz * star
            star_2d = self.ry * star_2d

            # find the intersection point between the star and the focus point
            star_2d = self.find_intersection(star_2d, normal)

            # if 2D star is within camera plane borders, add to list of stars to draw
            if (0 - self.width) < star_2d.item((1, 0)) < self.width and (0 - self.height) < star_2d.item((2, 0)) < self.height:
                # flip the screen over the vertical axis
                self.points.append((-star_2d.item((1, 0)), star_2d.item((2, 0))))

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
