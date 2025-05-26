from config import SATELLITE_GRID_SIZE
import random

class Satellite:
    def __init__(self, env):
        self.env = env

    def scan_for_hazards(self, car):
        """Simulates satellite scanning the region around a car with confidence levels."""
        car_region = self.get_region(car.x, car.y)
        detected = []

        for x in range(self.env.width):
            for y in range(self.env.height):
                if self.get_region(x, y) == car_region:
                    if self.env.check_hazard(x, y):
                        confidence = round(random.uniform(0.6, 0.99), 2)
                        detected.append((x, y, confidence))
        return detected

    def get_region(self, x, y):
        return (x // SATELLITE_GRID_SIZE, y // SATELLITE_GRID_SIZE)
