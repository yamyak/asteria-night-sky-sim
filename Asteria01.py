from Telescope import Telescope
from StarChart import StarChart
from Compass import Compass

if __name__ == "__main__":

    compass = Compass()
    compass.load_file("./config/z_positive.cfg")
    #compass.load_data(0.5, 0.5, 250, 250, (0, 0, 0), (1, 0, 0))
    scope = Telescope(compass)

    chart = StarChart()
    chart.load_file("./data/z_positive.csv")
    #chart.load_data([(100, 10, 10), (100, -20, 20), (100, -30, -30), (100, 40, -40)])
    scope.load_chart(chart)

    scope.calculate_view()
    scope.update_view()
