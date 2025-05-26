import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import os
import time
import random
import threading
import psutil
from config import LOG_FOLDER, SIMULATION_STEPS
from environment import SimulationEnvironment
from car import Car
from satellite import Satellite  # We'll treat "drones" as mobile satellite
from logger import Logger
from region_manager import RegionManager

def profile(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        print(f"[Profiler] {func.__name__} took {time.time() - start:.4f}s")
        return result
    return wrapper

def monitor_resources():
    process = psutil.Process(os.getpid())
    cpu = psutil.cpu_percent(interval=None)
    mem = process.memory_info().rss / (1024 * 1024)
    print(f"[Resource Monitor] CPU: {cpu:.2f}%, Memory: {mem:.2f} MB")

def get_distance(x1, y1, x2, y2):
    return ((x1 - x2)**2 + (y1 - y2)**2) ** 0.5

@profile
def run_step(step, cars, env, logger, satellite, region_manager, v2v_memory):
    env.step()

    def detect_and_log(car):
        hazards = car.detect_hazards()
        for hx, hy in hazards:
            v2v_memory[(hx, hy)] = v2v_memory.get((hx, hy), []) + [car.car_id]
            car.intelligence_score += 1
            logger.record_detection(step, car.car_id, hx, hy)

    threads = []
    for car in cars:
        thread = threading.Thread(target=detect_and_log, args=(car,))
        threads.append(thread)
        thread.start()
    for t in threads:
        t.join()

    # V2V sharing
    for car in cars:
        for (hx, hy), sharers in v2v_memory.items():
            if car.car_id not in sharers and random.random() < 0.85:
                car.receive_hazard(hx, hy)
                logger.record_received(step, car.car_id, hx, hy, sender_id=None)

    # Drone-car sync: localized drone update within radius
    for car in cars:
        for dx in range(-2, 3):
            for dy in range(-2, 3):
                nx, ny = car.x + dx, car.y + dy
                if 0 <= nx < env.width and 0 <= ny < env.height and env.check_hazard(nx, ny):
                    distance = get_distance(car.x, car.y, nx, ny)
                    confidence = max(0.7, 1.0 - distance / 10)
                    if random.random() < confidence:
                        car.receive_hazard(nx, ny)
                        car.intelligence_score += int(confidence * 5)
                        logger.record_satellite_info(step, car.car_id, nx, ny, confidence)

def main():
    os.makedirs(LOG_FOLDER, exist_ok=True)

    env = SimulationEnvironment()
    satellite = Satellite(env)
    region_manager = RegionManager()
    logger = Logger()
    cars = [Car(i, env, logger, region_manager, satellite) for i in range(env.num_cars)]

    v2v_memory = {}

    for step in range(SIMULATION_STEPS):
        run_step(step, cars, env, logger, satellite, region_manager, v2v_memory)
        monitor_resources()

    logger.save(cars)

if __name__ == "__main__":
    main()
    from visualizer import visualize_results
    visualize_results()