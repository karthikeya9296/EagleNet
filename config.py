import os
import shutil
import inspect

# === BASE PATHS ===
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)

# === DETECT TEST NAME FROM CALLING FILE ===
def get_test_name():
    stack = inspect.stack()
    for frame in stack:
        if frame.filename.endswith(".py") and "test_" in os.path.basename(frame.filename):
            name = os.path.splitext(os.path.basename(frame.filename))[0]
            return name.replace("test_", "")
    return "default"

TEST_NAME = get_test_name().replace("_", "-")  # e.g., shared-vision

# === FINAL FOLDER PATHS ===
LOG_FOLDER = os.path.join(DATA_DIR, "logs", TEST_NAME)
RESULTS_FOLDER = os.path.join(DATA_DIR, "results", TEST_NAME)

# === CLEAN FOLDERS (SAFELY) ===
def clean_folder(path):
    if os.path.exists(path):
        shutil.rmtree(path)
    os.makedirs(path)

clean_folder(LOG_FOLDER)
clean_folder(RESULTS_FOLDER)

# === GRID & SIMULATION PARAMETERS ===
GRID_WIDTH = 10
GRID_HEIGHT = 10
NUM_CARS = 20
HAZARD_SPAWN_RATE = 0.2
# === NUMBER OF STEPS FOR EACH SIMULATION RUN ===
SIMULATION_STEPS = 500  # or however many steps you want
# === SATELLITE SYSTEM PARAMETERS ===
SATELLITE_GRID_SIZE = 10  # or any appropriate grid dimension
