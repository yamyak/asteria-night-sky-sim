from StarChart import StarChart
from Telescope import Telescope

if __name__ == "__main__":
    chart = StarChart()
    scope = Telescope(0.5, 0.5, 250, 250, (0, 0, 0), (1, 0, 0))
    data = [(100, 0, 0), (100, -10, -10), (100, 10, 10)]
    chart.load_data(data)
    scope.calculate_view(chart.find_nearby_stars((0, 0, 0), (0, 0, 0)))
    scope.update_view()
