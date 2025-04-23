import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

def generate_telemetry_data(num_nodes=100, days=10, interval_minutes=10):
    timestamps = pd.date_range(end=datetime.now(), periods=(days * 24 * 60) // interval_minutes, freq=f'{interval_minutes}min')
    data = []

    for node in range(num_nodes):
        node_id = f"NODE-{1000 + node}"
        for ts in timestamps:
            cpu = np.random.normal(loc=30, scale=10)
            latency = np.random.normal(loc=20, scale=5)
            throughput = np.random.normal(loc=100, scale=20)
            packet_loss = np.random.uniform(0, 5)
            temp = np.random.normal(loc=60, scale=5)
            error_rate = np.random.exponential(scale=0.5)

            label = int(cpu > 70 or packet_loss > 3 or temp > 80 or error_rate > 1.5)

            data.append([node_id, ts, cpu, latency, throughput, packet_loss, temp, error_rate, label])

    columns = ["node_id", "timestamp", "cpu_usage", "latency", "throughput", "packet_loss", "temperature", "error_rate", "failure_label"]
    return pd.DataFrame(data, columns=columns)

df = generate_telemetry_data()
df.to_csv("data/simulated_network_telemetry.csv", index=False)
print("✅ Data simulation complete!")
