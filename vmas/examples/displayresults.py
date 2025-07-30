import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# read from results.csv
data = pd.read_csv("results.csv", header=None, names=["algorithm", "seed", "num_agents", "num_collisions", "time"])

# collision and time points
c_pts = []
t_pts = []

# create x, y coordinates for data in diff colliisions and diff time
for i, (a, b) in enumerate(zip(data["num_collisions"][::2], data["num_collisions"][1::2])):
    c_pts.append((int(data.iloc[i*2]["num_agents"]), (b - a)))

for i, (a, b) in enumerate(zip(data["time"][::2], data["time"][1::2])):
    t_pts.append((int(data.iloc[i*2]["num_agents"]), (b - a)))


# IQR-based outlier filtering using pandas
# Convert to DataFrame for easier filtering
c_df = pd.DataFrame(c_pts, columns=["num_agents", "delta_collisions"])
t_df = pd.DataFrame(t_pts, columns=["num_agents", "delta_time"])

# IQR filtering for collisions
Q1_c = c_df["delta_collisions"].quantile(0.25)
Q3_c = c_df["delta_collisions"].quantile(0.75)
IQR_c = Q3_c - Q1_c
c_df_filtered = c_df[(c_df["delta_collisions"] >= Q1_c - 1.5 * IQR_c) & 
                     (c_df["delta_collisions"] <= Q3_c + 1.5 * IQR_c)]

# IQR filtering for time
Q1_t = t_df["delta_time"].quantile(0.25)
Q3_t = t_df["delta_time"].quantile(0.75)
IQR_t = Q3_t - Q1_t
t_df_filtered = t_df[(t_df["delta_time"] >= Q1_t - 1.5 * IQR_t) & 
                     (t_df["delta_time"] <= Q3_t + 1.5 * IQR_t)]

# Extract filtered x and y data
x1, y1 = c_df_filtered["num_agents"], c_df_filtered["delta_collisions"]
x2, y2 = t_df_filtered["num_agents"], t_df_filtered["delta_time"]

# Calculate medians for each number of agents
c_medians = c_df_filtered.groupby("num_agents")["delta_collisions"].mean().reset_index()
t_medians = t_df_filtered.groupby("num_agents")["delta_time"].mean().reset_index()

# Create two stacked subplots with shared x-axis
fig, (ax1, ax2) = plt.subplots(nrows=2, sharex=True, figsize=(10, 6))

# Top plot
ax1.plot(x1, y1, marker='o', linestyle='None', markersize=4)
ax1.plot(c_medians["num_agents"], c_medians["delta_collisions"], marker='o', color='orange', linestyle='-', markersize=6, label='mean')
ax1.set_xlabel("Number of agents")
ax1.set_ylabel("delta collisions (no planning - planning)")
ax1.grid(True)
ax1.legend()

# Bottom plot
ax2.plot(x2, y2, marker='o', linestyle='None', markersize=4)
ax2.plot(t_medians["num_agents"], t_medians["delta_time"], marker='o', color='orange', linestyle='-', markersize=6, label='mean')
ax2.set_xlabel("Number of agents")
ax2.set_ylabel("delta time (no planning - planning)")
ax2.grid(True)
ax2.legend()

# Adjust spacing
plt.tight_layout()
plt.show()