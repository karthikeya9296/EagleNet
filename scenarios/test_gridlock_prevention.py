import sys
import os
import time
import random
import threading
import psutil
import pandas as pd

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import LOG_FOLDER, SIMULATION_STEPS
from environment import SimulationEnvironment
from car import Car
from satellite import Satellite
from logger import Logger
from region_manager import RegionManager
from utils import get_distance


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


@profile
def run_step(step, cars, env, logger, satellite, region_manager, hazard_aggregate, avoidance_threshold=3):
    env.step()

    def detect_and_log(car):
        local_hazards = []
        hazards = car.detect_hazards()
        for hx, hy in hazards:
            local_hazards.append((hx, hy))
            hazard_aggregate[(hx, hy)] = hazard_aggregate.get((hx, hy), 0) + 1
            car.intelligence_score += 1
            logger.record_detection(step, car.car_id, hx, hy)

        # If car is in a gridlock-prone area, reduce activity
        nearby_hazards = sum(
            1 for (hx, hy), count in hazard_aggregate.items()
            if get_distance(car.x, car.y, hx, hy) < 2
        )
        if nearby_hazards < avoidance_threshold:
            for (hx, hy), count in hazard_aggregate.items():
                if random.random() < 0.85:
                    car.receive_hazard(hx, hy)
                    logger.record_received(step, car.car_id, hx, hy, sender_id=None)

            satellite_data = satellite.scan_for_hazards(car)
            for hx, hy, confidence in satellite_data:
                if confidence > 0.7:
                    car.receive_hazard(hx, hy)
                    car.intelligence_score += int(confidence * 10)
                    logger.record_satellite_info(step, car.car_id, hx, hy, confidence)

    threads = []
    for car in cars:
        thread = threading.Thread(target=detect_and_log, args=(car,))
        threads.append(thread)
        thread.start()
    for t in threads:
        t.join()


def main():
    env = SimulationEnvironment()
    satellite = Satellite(env)
    region_manager = RegionManager()
    logger = Logger()
    cars = [Car(i, env, logger, region_manager, satellite) for i in range(env.num_cars)]

    for car in cars:
        car.intelligence_score = 0

    hazard_aggregate = {}

    for step in range(SIMULATION_STEPS):
        run_step(step, cars, env, logger, satellite, region_manager, hazard_aggregate)
        monitor_resources()

    logger.save(cars)


if __name__ == "__main__":
    main()

    # Optional plot fix: clean satellite_info if it exists
    from visualizer import visualize_results
    import os

    satellite_path = os.path.join(LOG_FOLDER, "satellite_info.csv")
    if os.path.exists(satellite_path):
        try:
            df = pd.read_csv(satellite_path)
            if "confidence" in df.columns:
                df["confidence"] = pd.to_numeric(df["confidence"], errors="coerce").fillna(0)
                df.to_csv(satellite_path, index=False)
        except Exception as e:
            print(f"⚠️ Satellite data cleanup failed: {e}")

    try:
        visualize_results()
    except Exception as e:
        print(f"⚠️ Visualization error: {e}")