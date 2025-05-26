import sys
import os
import shutil

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from simulation_run import main
from visualizer import visualize_results, run_live_animation
from config import LOG_FOLDER, RESULTS_FOLDER

# 🔀 Toggle this to enable real-time animation
USE_LIVE_ANIMATION = False  # ← Change to True for live matplotlib animation

def clean_previous_data():
    if os.path.exists(LOG_FOLDER):
        shutil.rmtree(LOG_FOLDER)
    if os.path.exists(RESULTS_FOLDER):
        shutil.rmtree(RESULTS_FOLDER)

if __name__ == "__main__":
    print("🧹 Cleaning old logs and results...")
    clean_previous_data()

    print("🚀 Running GridSight simulation...")
    main()

    if USE_LIVE_ANIMATION:
        print("🎞 Launching real-time detection animation...")
        run_live_animation()
    else:
        print("📊 Generating static graphs...")
        visualize_results()

    print("\n✅ Test complete. Data and graphs saved.")
