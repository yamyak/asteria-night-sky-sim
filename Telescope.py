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

        # Initialize pygame screen
        pygame.init()
        self.screen = pygame.display.set_mode((screen_w*2, screen_h*2))
        # self.screen.fill((0, 0, 0))

        self.focus_point = (np.asmatrix(focus_point)).T
        self.plane_point = (np.asmatrix(plane_point)).T
        self.polar = self.convert_to_polar(plane_point)

        self.rz = 0
        self.ry = 0
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
        phi = -self.polar[1]
        theta = (math.pi / 2) - self.polar[0]
        self.rz = np.matrix([[math.cos(phi), -math.sin(phi), 0],
                            [math.sin(phi), math.cos(phi), 0],
                            [0, 0, 1]])
        self.ry = np.matrix([[math.cos(theta), 0, math.sin(theta)],
                            [0, 1, 0],
                            [-math.sin(theta), 0, math.cos(theta)]])

    def calculate_view2(self, star_list):
        normal = self.plane_point - self.focus_point
        normal = self.rz * normal
        normal = self.ry * normal

        # iterate through list of stars
        for star in star_list:
            star_2d = self.rz * star
            star_2d = self.ry * star_2d

            star_2d = self.find_intersection2(star_2d, normal)

            # if point is within camera plane borders, add to list of points
            if (0 - self.width) < star_2d.item((1, 0)) < self.width and (0 - self.height) < star_2d.item((2, 0)) < self.height:
                self.points.append((star_2d.item((1, 0)), star_2d.item((2, 0))))

    def find_intersection2(self, star, normal):
        """
        Determine the intersection point of the star on the viewing plane
        :param star: 3d point to be transposed onto viewing plane
        :param normal: normal vector to viewing plane
        :return: 3d point on the viewing plane
        """
        d = (normal.T * normal) / ((star - self.focus_point).T * normal)

        return (d.item(0, 0) * (star - self.focus_point)) + self.focus_point

    def change_location(self, focus_point, plane_point):
        self.screen.fill(0, 0, 0)
        self.focus_point = focus_point
        self.plane_point = plane_point

    @staticmethod
    def find_max_index(vector):
        """
        Find the index of the largest absolute value in the vector
        :param vector: input vector of 3 points
        :return: index of largest absolute value in vector
        """
        max_index = 0
        max_value = 0

        # iterate through vector and find maximum value
        for i in range(vector.size):
            if math.fabs(vector[i]) > max_value:
                max_index = i
                max_value = math.fabs(vector[i])

        return max_index

    def create_orthonormal_basis(self, normal):
        """
        Creates an orthonormal basis based on the normal vector given
        :param normal: normal vector that basis is created from
        :return: orthonormal basis created
        """
        # Adds the normal vector as the first element of the basis
        # Zeros out the next 2 elements
        basis = [normal, np.array([0, 0, 0]), np.array([0, 0, 0])]
        basis_out = [normal, 0, 0]

        # get the maximum index value
        max_index = self.find_max_index(basis[0])

        # in zeroed out elements in basis array, set none max index values to 1
        basis[1][(max_index + 1) % 3] = 1
        basis[2][(max_index + 2) % 3] = 1

        # apply orthonormal basis algorithm to calculate next 2 values of orthonormal basis
        factor2 = np.dot(basis_out[0], basis[1]) / np.dot(basis_out[0], basis_out[0])
        basis_out[1] = basis[1] - factor2 * basis_out[0]

        factor2 = np.dot(basis_out[0], basis[2]) / np.dot(basis_out[0], basis_out[0])
        factor3 = np.dot(basis_out[1], basis[2]) / np.dot(basis_out[1], basis_out[1])
        basis_out[2] = basis[2] - factor2 * basis_out[0] - factor3 * basis_out[1]

        for i in range(0, 3):
            basis_out[i] = basis_out[i] / math.sqrt(np.dot(basis_out[i], basis_out[i]))

        return basis_out

    def find_intersection(self, star, normal):
        """
        Determine the intersection point of the star on the viewing plane
        :param star: 3d point to be transposed onto viewing plane
        :param normal: normal vector to viewing plane
        :return: 3d point on the viewing plane
        """
        d = np.dot((self.plane_point - self.focus_point), normal) / np.dot((star - self.focus_point), normal)

        return (d * (star - self.focus_point)) + self.focus_point

    @staticmethod
    def affine_transform(basis, point_3d):
        """
        Perform an affine transform on the plane point to set it to the correct coordinate system
        :param basis: orthonormal basis
        :param point_3d: 3d viewing plane point
        :return: 2d point transformed onto the correct coordinate system
        """
        x = np.dot(point_3d, basis[0])
        y = np.dot(point_3d, basis[1])
        z = np.dot(point_3d, basis[2])
        #point = [point[0] - self.plane_point[0], point[1] - self.plane_point[1]]
        #point = [point3[2], point3[1]]

        return z, y

    def calculate_view(self, star_list):
        """
        Transposed a set of 3d points onto their 2d counterparts on a 2d plane
        :param star_list: list of stars (3d points) to be transposed onto viewing plane
        """
        # calculate the normal to the plane
        normal = self.plane_point - self.focus_point

        # normalize the normal
        normalized = normal / math.sqrt(np.dot(normal, normal))

        # calculate orthonormal basis
        basis = self.create_orthonormal_basis(normalized)

        # iterate through list of stars
        for star in star_list:
            intersection = self.find_intersection(star, normal)
            point = self.affine_transform(basis, intersection)

            # if point is within camera plane borders, add to list of points
            if (0 - self.width) < point[0] < self.width and (0 - self.height) < point[1] < self.height:
                self.points.append(point)

    def update_view(self):
        for entry in self.points:
            x = entry[0] * self.screen_w / self.width + self.screen_w
            y = self.screen_h*2 - (entry[1] * self.screen_h / self.height + self.screen_h)

            pygame.draw.circle(self.screen, (0, 255, 0), (int(x), int(y)), 1, 0)

        pygame.display.update()

        test = True
