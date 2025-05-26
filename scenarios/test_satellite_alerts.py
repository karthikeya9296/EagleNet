# test_satellite_alerts.py
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from simulation_run import main
from visualizer import visualize_results

print("🛰️ Running Satellite Alerts scenario...")
main()
print("📊 Generating visualizations...")
visualize_results()
print("✅ Satellite Alerts scenario completed.")
