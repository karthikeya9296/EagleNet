# test_pedestrian_edge_awareness.py
import sys
import os
import threading

# Fix module path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from simulation_run import run_step
from logger import Logger
from config import LOG_FOLDER, SIMULATION_STEPS
from car import Car
from satellite import Satellite
from environment import SimulationEnvironment
from region_manager import RegionManager
from visualizer import visualize_results

# Initialize core components
env = SimulationEnvironment()
satellite = Satellite(env)
region_manager = RegionManager()
logger = Logger()
cars = [Car(i, env, logger, region_manager, satellite) for i in range(env.num_cars)]

# Prepare V2V memory for run_step
v2v_memory = {}

# Function to detect cars at grid edges
def detect_and_log(car):
    if car.x in [0, env.grid_size - 1] or car.y in [0, env.grid_size - 1]:
        logger.log_event("EdgeAlert", {
            "car_id": car.car_id,
            "x": car.x,
            "y": car.y
        })

# Main simulation loop
for step in range(SIMULATION_STEPS):
    run_step(step, cars, env, logger, satellite, region_manager, v2v_memory)

    threads = []
    for car in cars:
        t = threading.Thread(target=detect_and_log, args=(car,))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()

# Save logs and visualize results
logger.save(cars)
visualize_results()