from Telescope import Telescope
from StarChart import StarChart
from Compass import Compass

if __name__ == "__main__":

    compass = Compass()
    compass.load_data(0.5, 0.5, 250, 250, (0, 0, 0), (1, 0, 0))
    #compass.load_data(0.5, 0.5, 250, 250, (0, 0, 0), (-1, 0, 0))
    #compass.load_data(0.5, 0.5, 250, 250, (0, 0, 0), (0, 1, 0))
    #compass.load_data(0.5, 0.5, 250, 250, (0, 0, 0), (0, -1, 0))
    #compass.load_data(0.5, 0.5, 250, 250, (0, 0, 0), (0, 0, 1))
    #compass.load_data(0.5, 0.5, 250, 250, (0, 0, 0), (0, 0, -1))
    scope = Telescope(compass)

    chart = StarChart()
    data = [(100, 10, 10), (100, -20, 20), (100, -30, -30), (100, 40, -40)]
    #data = [(-100, 10, 10), (-100, -20, 20), (-100, -30, -30), (-100, 40, -40)]
    #data = [(10, 100, 10), (-20, 100, 20), (-30, 100, -30), (40, 100, -40)]
    #data = [(10, -100, 10), (-20, -100, 20), (-30, -100, -30), (40, -100, -40)]
    #data = [(10, 10, 100), (-20, 20, 100), (-30, -30, 100), (40, -40, 100)]
    #data = [(10, 10, -100), (-20, 20, -100), (-30, -30, -100), (40, -40, -100)]
    chart.load_data(data)
    scope.load_chart(chart)

    scope.calculate_view()
    scope.update_view()
