# utils/logger.py

import os
import csv
from datetime import datetime

LOGS_DIR = "logs"
os.makedirs(LOGS_DIR, exist_ok=True)


def log_prediction(username, image_name, label, confidence):
    """
    Appends a log entry per user.
    """
    log_file = os.path.join(LOGS_DIR, f"{username}_logs.csv")
    log_entry = [image_name, label, f"{confidence:.4f}", datetime.now().strftime("%Y-%m-%d %H:%M:%S")]

    with open(log_file, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(log_entry)


def get_user_logs(username):
    """
    Returns logs for given username as list of rows.
    """
    log_file = os.path.join(LOGS_DIR, f"{username}_logs.csv")
    if not os.path.exists(log_file):
        return []

    with open(log_file, "r") as f:
        reader = csv.reader(f)
        return list(reader)
