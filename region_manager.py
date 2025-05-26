from config import SATELLITE_GRID_SIZE

class RegionManager:
    def __init__(self):
        pass  # No setup needed for now

    def get_region(self, x, y):
        return (x // SATELLITE_GRID_SIZE, y // SATELLITE_GRID_SIZE)
