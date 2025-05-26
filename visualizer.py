import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.animation as animation
from matplotlib import cm
from config import LOG_FOLDER, RESULTS_FOLDER


def save_plot(fig, name):
    os.makedirs(RESULTS_FOLDER, exist_ok=True)
    fig.savefig(os.path.join(RESULTS_FOLDER, name), bbox_inches='tight')
    plt.close(fig)


def try_load(name):
    path = os.path.join(LOG_FOLDER, name)
    return pd.read_csv(path) if os.path.exists(path) else None


def visualize_results(real_time=False):
    detections = try_load("detection_density.csv")
    car_counts = try_load("car_detection_count.csv")
    satellite_info = try_load("satellite_info.csv")
    receptions = try_load("hazard_reception_counts.csv")
    intelligence = try_load("intelligence_scores.csv")

    if detections is not None:
        fig = plt.figure(figsize=(8, 6))
        plt.title("Hazard Detections Heatmap")
        sns.kdeplot(
            x=detections["x"],
            y=detections["y"],
            fill=True,
            cmap="Reds",
            bw_adjust=0.5,
            levels=50,
            thresh=0.05,
        )
        plt.xlabel("Hazard Grid X Coordinate")
        plt.ylabel("Hazard Grid Y Coordinate")
        save_plot(fig, "hazard_detections.png")

    if car_counts is not None:
        fig = plt.figure(figsize=(10, 4))
        plt.title("Hazards Detected by Each Car")
        plt.xlabel("Car ID")
        plt.ylabel("Hazards Detected")
        plt.bar(car_counts["car_id"], car_counts["detection_count"], color="steelblue")
        save_plot(fig, "shared_vision.png")

    if satellite_info is not None:
        fig = plt.figure(figsize=(10, 6))
        plt.title("Satellite Insight: Hazard Locations and Confidence")
        plt.xlabel("Hazard Grid X Coordinate")
        plt.ylabel("Hazard Grid Y Coordinate")
        plt.scatter(
            satellite_info["hazard_x"],
            satellite_info["hazard_y"],
            s=satellite_info["confidence"] * 80,
            alpha=0.6,
            c="green",
            edgecolors="black"
        )
        save_plot(fig, "satellite_insight.png")

    if receptions is not None:
        fig = plt.figure(figsize=(8, 6))
        plt.title("Hazard Broadcast Reach per Coordinate")
        plt.xlabel("Hazard Grid X Coordinate")
        plt.ylabel("Hazard Grid Y Coordinate")
        plt.scatter(
            receptions["x"],
            receptions["y"],
            s=receptions["cars_received"] * 10,
            alpha=0.7,
            c="purple",
            edgecolors="black"
        )
        for _, row in receptions.iterrows():
            plt.text(
                row["x"], row["y"], str(row["cars_received"]),
                fontsize=7, ha='center', va='center'
            )
        save_plot(fig, "reception_counts.png")

    if intelligence is not None:
        fig = plt.figure(figsize=(10, 4))
        plt.title("Car Intelligence Scores")
        plt.xlabel("Car ID")
        plt.ylabel("Intelligence Score")
        plt.bar(intelligence["car_id"], intelligence["intelligence_score"], color="orange")
        save_plot(fig, "intelligence_scores.png")

    if real_time:
        print("⚠️ Real-time animation requires GUI and blocks execution. Use only in desktop sessions.")


def run_live_animation():
    path = os.path.join(LOG_FOLDER, "detections.csv")
    if not os.path.exists(path):
        print("No detection log found for animation.")
        return

    df = pd.read_csv(path)
    fig, ax = plt.subplots()
    sc = ax.scatter([], [], c=[], cmap=cm.plasma, s=80)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.set_title("Live Hazard Detection Replay")
    ax.set_xlabel("Grid X Coordinate")
    ax.set_ylabel("Grid Y Coordinate")

    def update(frame):
        current = df[df["step"] == frame]
        sc.set_offsets(current[["x", "y"]])
        sc.set_array(current["car_id"])
        return sc,

    frames = df["step"].max() + 1
    ani = animation.FuncAnimation(fig, update, frames=frames, interval=200, blit=True)
    plt.show()
