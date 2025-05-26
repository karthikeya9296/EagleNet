import random
from config import GRID_WIDTH, GRID_HEIGHT

class Car:
    def __init__(self, car_id, env, logger, region_manager, satellite):
        self.intelligence_score = 0
        self.car_id = car_id
        self.env = env
        self.logger = logger
        self.region_manager = region_manager
        self.satellite = satellite
        self.x = random.randint(0, GRID_WIDTH - 1)
        self.y = random.randint(0, GRID_HEIGHT - 1)
        self.known_hazards = set()

    def move(self):
        self.x = max(0, min(self.x + random.choice([-1, 0, 1]), GRID_WIDTH - 1))
        self.y = max(0, min(self.y + random.choice([-1, 0, 1]), GRID_HEIGHT - 1))

    def detect_hazards(self):
        hazards_detected = []
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                nx = self.x + dx
                ny = self.y + dy
                if 0 <= nx < self.env.width and 0 <= ny < self.env.height:
                    if self.env.check_hazard(nx, ny):
                        hazards_detected.append((nx, ny))
        return hazards_detected

    def receive_hazard(self, x, y):
        if (x, y) not in self.known_hazards:
            self.known_hazards.add((x, y))
