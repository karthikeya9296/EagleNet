# scenarios/test_pothole_mapping.py
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import random
from simulation_run import run_step
from environment import SimulationEnvironment
from car import Car
from satellite import Satellite
from logger import Logger
from region_manager import RegionManager
from config import SIMULATION_STEPS

def pothole_mapping_scenario():
    print("Running Pothole Mapping Scenario...")

    env = SimulationEnvironment()
    satellite = Satellite(env)
    region_manager = RegionManager()
    logger = Logger()
    cars = [Car(i, env, logger, region_manager, satellite) for i in range(env.num_cars)]

    for car in cars:
        car.intelligence_score = 0

    env.set_cars(cars)

    # Add fixed potholes to the map
    pothole_locations = [(2, 2), (5, 5), (7, 3), (1, 8)]
    for x, y in pothole_locations:
        env.hazards.add((x, y))  # Simulating pothole spawn

    v2v_memory = {}

    for step in range(SIMULATION_STEPS):
        run_step(step, cars, env, logger, satellite, region_manager, v2v_memory)

    logger.save(cars)
    print("Pothole Mapping Scenario completed and logs saved.")

if __name__ == "__main__":
    pothole_mapping_scenario()
    from visualizer import visualize_results
    visualize_results()