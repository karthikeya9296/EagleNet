import os
import csv
import json
from collections import defaultdict
from config import LOG_FOLDER

class Logger:
    def __init__(self):
        self.detections = []
        self.received = []
        self.events = []
        self.satellite_info = []
        self.detection_density = defaultdict(int)
        self.car_detection_count = defaultdict(int)
        self.reception_counts = defaultdict(int)
        self.intelligence_scores = defaultdict(int)

        self.global_satellite_logged = set()
        self._detection_set = set()
        self._received_set = set()
        self._satellite_set = set()

        os.makedirs(LOG_FOLDER, exist_ok=True)

    def record_detection(self, step, car_id, x, y):
        key = (car_id, x, y)
        if key not in self._detection_set:
            self._detection_set.add(key)
            self.detections.append((step, car_id, x, y))
            self.detection_density[(x, y)] += 1
            self.car_detection_count[car_id] += 1
            print(f"Car {car_id} detected hazard at ({x}, {y})")

    def record_received(self, step, car_id, hx, hy, sender_id=None):
        key = (car_id, hx, hy)
        if key not in self._received_set:
            self._received_set.add(key)
            self.received.append((step, car_id, hx, hy, sender_id))
            self.reception_counts[(hx, hy)] += 1
            print(f"Car {car_id} received hazard info about ({hx}, {hy}) from Car {sender_id}")

    def record_satellite_info(self, step, car_id, hx, hy, confidence):
        global_key = (hx, hy)
        if global_key not in self.global_satellite_logged:
            self.global_satellite_logged.add(global_key)
            self.satellite_info.append((step, car_id, hx, hy, confidence))
            print(f"Car {car_id} got satellite data for hazard at ({hx}, {hy}) with confidence {confidence}")

    def record_intelligence(self, car_id, score):
        self.intelligence_scores[car_id] = score

    def log_event(self, event_type, event_data):
        self.events.append({"type": event_type, "data": event_data})
        print(f"[LOG - {event_type}] {event_data}")

    def save(self, cars=None):
        # CSVs
        with open(os.path.join(LOG_FOLDER, "detections.csv"), "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["step", "car_id", "x", "y"])
            writer.writerows(self.detections)

        with open(os.path.join(LOG_FOLDER, "received.csv"), "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["step", "car_id", "hazard_x", "hazard_y", "sender_id"])
            writer.writerows(self.received)

        with open(os.path.join(LOG_FOLDER, "satellite_info.csv"), "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["step", "car_id", "hazard_x", "hazard_y", "confidence"])
            writer.writerows(self.satellite_info)

        with open(os.path.join(LOG_FOLDER, "detection_density.csv"), "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["x", "y", "detection_count"])
            for (x, y), count in self.detection_density.items():
                writer.writerow([x, y, count])

        with open(os.path.join(LOG_FOLDER, "car_detection_count.csv"), "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["car_id", "detection_count"])
            for car_id, count in self.car_detection_count.items():
                writer.writerow([car_id, count])

        with open(os.path.join(LOG_FOLDER, "hazard_reception_counts.csv"), "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["x", "y", "cars_received"])
            for (x, y), count in self.reception_counts.items():
                writer.writerow([x, y, count])

        with open(os.path.join(LOG_FOLDER, "intelligence_scores.csv"), "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["car_id", "intelligence_score"])
            for car_id, score in self.intelligence_scores.items():
                writer.writerow([car_id, score])

        # JSON exports
        with open(os.path.join(LOG_FOLDER, "detections.json"), "w") as f:
            json.dump([{"step": s, "car_id": cid, "x": x, "y": y} for (s, cid, x, y) in self.detections], f, indent=2)

        with open(os.path.join(LOG_FOLDER, "satellite_info.json"), "w") as f:
            json.dump([{"step": s, "car_id": cid, "x": x, "y": y, "confidence": conf} for (s, cid, x, y, conf) in self.satellite_info], f, indent=2)

        if cars:
            # Redundant safeguard in case scores were missed during simulation
            with open(os.path.join(LOG_FOLDER, "intelligence_scores.csv"), "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["car_id", "intelligence_score"])
                for car in cars:
                    writer.writerow([car.car_id, getattr(car, "intelligence_score", 0)])
