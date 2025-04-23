import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from sklearn.ensemble import RandomForestClassifier

# ========================
# 🌈 Custom Streamlit Theme Header
# ========================
st.markdown("""
<h1 style='text-align: center; color: #42f5b9;'>🛰 Digital Twin</h1>
<h3 style='text-align: center; color: white;'>Real-Time Node Health Monitoring & Failure Risk</h3>
""", unsafe_allow_html=True)

# ========================
# 📥 Load and preprocess data
# ========================
df = pd.read_csv("Data/processed_network_data.csv")
df["timestamp"] = pd.to_datetime(df["timestamp"])

# Sidebar - Node ID selector
node_id = st.sidebar.selectbox("🔍 Select Node ID", df["node_id"].unique())
node_data = df[df["node_id"] == node_id]
latest = node_data.sort_values("timestamp").iloc[-1]

# ========================
# 📊 Display key metrics
# ========================
st.subheader(f"📍 Latest Telemetry for {node_id}")

# Create a clean 5-column grid
col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("CPU Usage (%)", f"{latest['cpu_usage']:.2f}")
col2.metric("Latency (ms)", f"{latest['latency']:.2f}")
col3.metric("Packet Loss (%)", f"{latest['packet_loss']:.2f}")
col4.metric("Temperature (°C)", f"{latest['temperature']:.2f}")
col5.metric("Error Rate", f"{latest['error_rate']:.3f}")

# Optional: View raw data
with st.expander("📘 View Raw Latest Telemetry Data"):
    st.dataframe(latest.to_frame().T)

# ========================
# 🔍 Train local ML model (for demo purposes)
# ========================
features = ["cpu_usage", "latency", "throughput", "packet_loss", "temperature", "error_rate", "rolling_avg_cpu", "hour", "dayofweek"]
X = node_data[features]
y = node_data["failure_label"]

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)
failure_prob = model.predict_proba([latest[features]])[0][1]

# ========================
# 🚨 Failure risk display
# ========================
if failure_prob > 0.7:
    risk_status = "🟥 High"
elif failure_prob > 0.4:
    risk_status = "🟨 Medium"
else:
    risk_status = "🟩 Low"

st.markdown(f"### ⚠️ Failure Risk: {risk_status}")
st.progress(failure_prob)

# ========================
# 📊 Telemetry Trends Section (Multiple Charts)
# ========================
st.subheader("📊 Node Telemetry Trends Over Time")
sns.set_theme(style="darkgrid")

# Line chart for CPU Usage
st.markdown("**CPU Usage (%)**")
fig_cpu, ax_cpu = plt.subplots(figsize=(12, 4))
sns.lineplot(data=node_data, x="timestamp", y="cpu_usage", ax=ax_cpu, linewidth=1.2)
ax_cpu.xaxis.set_major_locator(mdates.AutoDateLocator())
ax_cpu.xaxis.set_major_formatter(mdates.DateFormatter("%b %d\n%H:%M"))
fig_cpu.autofmt_xdate(rotation=45)
ax_cpu.set_xlabel("Time")
ax_cpu.set_ylabel("CPU Usage")
st.pyplot(fig_cpu)

# Line chart for Temperature
st.markdown("**Temperature (°C)**")
fig_temp, ax_temp = plt.subplots(figsize=(12, 4))
sns.lineplot(data=node_data, x="timestamp", y="temperature", ax=ax_temp, linewidth=1.2, color="orange")
ax_temp.xaxis.set_major_locator(mdates.AutoDateLocator())
ax_temp.xaxis.set_major_formatter(mdates.DateFormatter("%b %d\n%H:%M"))
fig_temp.autofmt_xdate(rotation=45)
ax_temp.set_xlabel("Time")
ax_temp.set_ylabel("Temperature")
st.pyplot(fig_temp)

# Line chart for Latency
st.markdown("**Latency (ms)**")
fig_latency, ax_latency = plt.subplots(figsize=(12, 4))
sns.lineplot(data=node_data, x="timestamp", y="latency", ax=ax_latency, linewidth=1.2, color="red")
ax_latency.xaxis.set_major_locator(mdates.AutoDateLocator())
ax_latency.xaxis.set_major_formatter(mdates.DateFormatter("%b %d\n%H:%M"))
fig_latency.autofmt_xdate(rotation=45)
ax_latency.set_xlabel("Time")
ax_latency.set_ylabel("Latency")
st.pyplot(fig_latency)

# ========================
# 🧾 Footer
# ========================
st.markdown("---")
st.markdown("<div style='text-align: center;'>Built with ❤️ using PySpark, Scikit-learn & Streamlit</div>", unsafe_allow_html=True)
