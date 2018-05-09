import configparser as cp


class Compass:

    def __init__(self):
        self.width = 0
        self.height = 0
        self.screen_w = 0
        self.screen_h = 0
        self.focus_point = 0
        self.plane_point = 0

    def load_file(self, file_path):
        """
        Opens the INI file, reads in the data, and populates the compass
        :param file_path: path to the INI file
        """
        # open the INI file
        config = cp.ConfigParser()
        config.read(file_path)

        self.width = float(config['DEFAULT']['Width'])
        self.height = float(config['DEFAULT']['Height'])
        self.screen_w = int(config['DEFAULT']['ScreenWidth'])
        self.screen_h = int(config['DEFAULT']['ScreenHeight'])

        focus_point_x = int(config['FocusPoint']['X'])
        focus_point_y = int(config['FocusPoint']['Y'])
        focus_point_z = int(config['FocusPoint']['Z'])
        self.focus_point = (focus_point_x, focus_point_y, focus_point_z)

        plane_point_x = int(config['PlanePoint']['X'])
        plane_point_y = int(config['PlanePoint']['Y'])
        plane_point_z = int(config['PlanePoint']['Z'])
        self.plane_point = (plane_point_x, plane_point_y, plane_point_z)

    def load_data(self, width, height, screen_w, screen_h, focus_point, plane_point):
        """
        Populates the compass with input data
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

        self.focus_point = focus_point
        self.plane_point = plane_point
