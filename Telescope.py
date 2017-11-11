import pygame
import numpy as np
import math


class Telescope:

    def __init__(self, width, height, screen_w, screen_h, focus_point, plane_point):
        self.width = width
        self.height = height
        self.screen_w = screen_w
        self.screen_h = screen_h

        pygame.init()
        self.screen = pygame.display.set_mode((screen_w*2, screen_h*2))
        # self.screen.fill((0, 0, 0))

        self.focus_point = np.asarray(focus_point)
        self.plane_point = np.asarray(plane_point)

        self.points = []

    def change_location(self, focus_point, plane_point):
        self.screen.fill(0, 0, 0)
        self.focus_point = focus_point
        self.plane_point = plane_point

    @staticmethod
    def find_max_index(vector):
        max_index = 0
        max_value = 0

        for i in range(vector.size):
            if math.fabs(vector[i]) > max_value:
                max_index = i
                max_value = math.fabs(vector[i])

        return max_index

    def create_orthonormal_basis(self, normal):
        basis = [normal, np.array([0, 0, 0]), np.array([0, 0, 0])]
        basis_out = [normal, 0, 0]

        max_index = self.find_max_index(basis[0])

        basis[1][(max_index + 1) % 3] = 1
        basis[2][(max_index + 2) % 3] = 1

        factor2 = np.dot(basis_out[0], basis[1]) / np.dot(basis_out[0], basis_out[0])
        basis_out[1] = basis[1] - factor2 * basis_out[0]

        factor2 = np.dot(basis_out[0], basis[2]) / np.dot(basis_out[0], basis_out[0])
        factor3 = np.dot(basis_out[1], basis[2]) / np.dot(basis_out[1], basis_out[1])
        basis_out[2] = basis[2] - factor2 * basis_out[0] - factor3 * basis_out[1]

        for i in range(0, 3):
            basis_out[i] = basis_out[i] / math.sqrt(np.dot(basis_out[i], basis_out[i]))

        return basis_out

    def find_intersection(self, star, normal):
        d = np.dot((self.plane_point - self.focus_point), normal) / np.dot((star - self.focus_point), normal)

        return (d * (star - self.focus_point)) + self.focus_point

    @staticmethod
    def affine_transform(basis, point_3d):

        x = np.dot(point_3d, basis[0])
        y = np.dot(point_3d, basis[1])
        z = np.dot(point_3d, basis[2])

        return x, y, z

    def calculate_view(self, star_list):
        normal = self.plane_point - self.focus_point

        normalized = normal / math.sqrt(np.dot(normal, normal))

        basis = self.create_orthonormal_basis(normalized)

        for star in star_list:
            intersection = self.find_intersection(star, normal)
            point3 = self.affine_transform(basis, intersection)
            # point = [point[0] - self.plane_point[0], point[1] - self.plane_point[1]]
            point = [point3[2], point3[1]]

            if (0 - self.width) < point[0] < self.width and (0 - self.height) < point[1] < self.height:
                self.points.append(point)

    def update_view(self):
        for entry in self.points:
            x = entry[0] * self.screen_w / self.width + self.screen_w
            y = self.screen_h*2 - (entry[1] * self.screen_h / self.height + self.screen_h)

            pygame.draw.circle(self.screen, (0, 255, 0), (int(x), int(y)), 1, 0)

        pygame.display.update()
