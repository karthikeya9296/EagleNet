import os
import random
import time
import threading
import psutil
import pandas as pd
from config import LOG_FOLDER, SIMULATION_STEPS
from environment import SimulationEnvironment
from car import Car
from satellite import Satellite
from logger import Logger
from region_manager import RegionManager

def profile(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - start
        print(f"[Profiler] {func.__name__} took {elapsed:.4f}s")
        return result
    return wrapper

def monitor_resources():
    process = psutil.Process(os.getpid())
    cpu = psutil.cpu_percent(interval=None)
    mem = process.memory_info().rss / (1024 * 1024)
    print(f"[Resource Monitor] CPU: {cpu:.2f}%, Memory: {mem:.2f} MB")

@profile
def run_step(step, cars, env, logger, satellite, region_manager, v2v_memory):
    env.step()

    blackout = random.sample(range(env.num_cars), k=env.num_cars // 10)
    threads = []

    def detect_and_log(car):
        hazards = car.detect_hazards()
        for hx, hy in hazards:
            key = (hx, hy)
            v2v_memory[key] = v2v_memory.get(key, []) + [car.car_id]
            car.intelligence_score += 1  # Intelligence boost on detection
            logger.record_detection(step, car.car_id, hx, hy)

    for car in cars:
        thread = threading.Thread(target=detect_and_log, args=(car,))
        threads.append(thread)
        thread.start()

    for t in threads:
        t.join()

    # V2V sharing with latency/occlusion
    for car in cars:
        for (hx, hy), sharers in v2v_memory.items():
            if car.car_id not in sharers:
                if random.random() < 0.9:  # 90% success rate
                    car.receive_hazard(hx, hy)
                    logger.record_received(step, car.car_id, hx, hy, sender_id=None)

    # Satellite fallback
    for car in cars:
        if car.car_id in blackout:
            continue
        satellite_data = satellite.scan_for_hazards(car)
        for hx, hy, confidence in satellite_data:
            if confidence > 0.7:  # Confidence filter
                car.receive_hazard(hx, hy)
                car.intelligence_score += int(confidence * 10)
                logger.record_satellite_info(step, car.car_id, hx, hy, confidence)

def main():
    os.makedirs(LOG_FOLDER, exist_ok=True)

    env = SimulationEnvironment()
    satellite = Satellite(env)
    region_manager = RegionManager()
    logger = Logger()
    cars = [Car(i, env, logger, region_manager, satellite) for i in range(env.num_cars)]

    for car in cars:
        car.intelligence_score = 0

    v2v_memory = {}

    for step in range(SIMULATION_STEPS):
        run_step(step, cars, env, logger, satellite, region_manager, v2v_memory)
        monitor_resources()

    logger.save(cars)

if __name__ == "__main__":
    main()
