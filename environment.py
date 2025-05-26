from config import GRID_WIDTH, GRID_HEIGHT, HAZARD_SPAWN_RATE
import random

class SimulationEnvironment:
    def __init__(self,grid_size=20, num_cars=40):
        self.grid_size = grid_size
        self.num_cars = num_cars
        self.width = GRID_WIDTH
        self.height = GRID_HEIGHT
        self.num_cars = 20
        self.hazards = set()
        self.cars = []

    def step(self):
        if random.random() < HAZARD_SPAWN_RATE:
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            self.hazards.add((x, y))

    def check_hazard(self, x, y):
        return (x, y) in self.hazards

    def set_cars(self, cars):
        self.cars = cars

    def get_cars(self):
        return self.cars
    
    def add_hazard(self, x, y, hazard_type="unknown"):
        self.hazards.add((x, y))  # You can optionally store hazard_type if needed
