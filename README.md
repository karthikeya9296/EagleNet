
# GridSight: AI-Enhanced Autonomous Vehicle Simulation Framework

**GridSight** is a simulation system for evaluating intelligent hazard detection, V2V (vehicle-to-vehicle) communication, and satellite-assisted driving in complex traffic scenarios. This project models real-world situations to benchmark AI capabilities in autonomous fleets.

---

## 📁 Project Structure

```
.
├── data/
│   ├── logs/               # Raw logs per scenario (CSV/JSON)
│   ├── results/            # Output images per scenario
│   └── snapshots/          # Unused or WIP snapshot exports
├── scenarios/              # All test scenarios
├── *.py                    # Core modules (env, cars, satellite, logger)
├── README.md               # This file
└── structure.txt           # Directory tree
```

---

## 🚗 Scenarios Simulated

Below are all 10 intelligent driving scenarios tested in `scenarios/` with their associated **logs** and **visualizations**.

---

### 1. Pedestrian Edge Awareness

- Test: `scenarios/test_pedestrian_edge_awareness.py`
- Logs: `data/logs/pedestrian-edge-awareness/`
- Results:
  - `hazard_detections.png`
  - `reception_counts.png`
  - `intelligence_scores.png`
  - `satellite_insight.png`

---

### 2. Emergency Clear

- Test: `scenarios/test_emergency_clear.py`
- Logs: `data/logs/emergency-clear/`
- Results:
  - `hazard_detections.png`
  - `reception_counts.png`
  - `intelligence_scores.png`
  - `satellite_insight.png`

---

### 3. Shared Vision

- Test: `scenarios/test_shared_vision.py`
- Logs: `data/logs/shared-vision/`
- Results:
  - `hazard_detections.png`
  - `reception_counts.png`
  - `intelligence_scores.png`
  - `satellite_insight.png`

---

### 4. Gridlock Prevention

- Test: `scenarios/test_gridlock_prevention.py`
- Logs: `data/logs/gridlock-prevention/`
- Results:
  - `hazard_detections.png`
  - `reception_counts.png`
  - `intelligence_scores.png`
  - `satellite_insight.png`

---

### 5. Drone-Car Sync

- Test: `scenarios/test_drone_car_sync.py`
- Logs: `data/logs/drone-car-sync/`
- Results:
  - `hazard_detections.png`
  - `reception_counts.png`
  - `intelligence_scores.png`
  - `satellite_insight.png`

---

### 6. Grid Failure Rerouting

- Test: `scenarios/test_grid_failure_rerouting.py`
- Logs: `data/logs/grid-failure-rerouting/`
- Results:
  - `hazard_detections.png`
  - `reception_counts.png`
  - `intelligence_scores.png`
  - `satellite_insight.png`

---

### 7. Satellite Alerts

- Test: `scenarios/test_satellite_alerts.py`
- Logs: `data/logs/satellite-alerts/`
- Results:
  - `hazard_detections.png`
  - `reception_counts.png`
  - `intelligence_scores.png`
  - `satellite_insight.png`

---

### 8. Pothole Mapping

- Test: `scenarios/test_pothole_mapping.py`
- Logs: `data/logs/pothole-mapping/`
- Results:
  - `hazard_detections.png`
  - `reception_counts.png`
  - `intelligence_scores.png`
  - `satellite_insight.png`

---

### 9. Convoy Mode

- Test: `scenarios/test_convoy_mode.py`
- Logs: `data/logs/convoy-mode/`
- Results:
  - `hazard_detections.png`
  - `reception_counts.png`
  - `intelligence_scores.png`
  - `satellite_insight.png`

---

### 10. Vision Blackout Recovery

- Test: `scenarios/test_vision_blackout_recovery.py`
- Logs: `data/logs/vision-blackout-recovery/`
- Results:
  - `hazard_detections.png`
  - `reception_counts.png`
  - `intelligence_scores.png`
  - `satellite_insight.png`

---

## ⚙️ How to Run a Scenario

```bash
# Example: Run the Shared Vision simulation
python scenarios/test_shared_vision.py
```

---

## 📊 Key Metrics Tracked

Each scenario generates:

- `detections.csv`: All hazard detections per car
- `received.csv`: V2V-received hazards
- `intelligence_scores.csv`: Final intelligence score per car
- `satellite_info.csv/json`: Satellite fallback responses
- `car_detection_count.csv`: Detection count per car
- `detection_density.csv`: Grid-based heatmap info

Visualizations are saved in `data/results/[scenario-name]/*.png`.

---

## 🧠 Core Features

- AI hazard detection simulation
- Realistic communication loss
- Satellite-based recovery strategies
- Logging for benchmarking and research
- Image generation for each metric

---

## 🧾 Authors & Contact

GridSight AI Team  
📧 `gummadikarthikeya3@gmail.com`  
🧠 Patent pending  
🔬 Research paper in progress
