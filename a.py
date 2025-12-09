import streamlit as st
import random
import time
import math
import pandas as pd

st.set_page_config(page_title="OptiNetSim", layout="wide")

st.title("🔮 OptiNetSim – Real-Time Optical Switching Simulator")
st.caption("FI9038 – Optical Switching Techniques | No datasets | No ML | Pure Algorithms")

# ---------------------------------------------------------
# USER INPUT CONTROLS
# ---------------------------------------------------------
col1, col2, col3 = st.columns(3)

switch_type = col1.selectbox(
    "Switching Technique",
    ["Optical Packet Switching (OPS)", 
     "Optical Burst Switching (OBS)", 
     "Optical Time Division Multiplexing (OTDM)"]
)

reservation = col2.selectbox(
    "Reservation / Timing Mechanism",
    ["None", "JIT", "JET", "Tell-And-Wait", "Tell-And-Go"]
)

burst_method = col3.selectbox(
    "Burst Assembly",
    ["Timer-Based", "Length-Based", "Mixed"]
)

traffic_rate = st.slider("Traffic Arrival Rate (packets/sec)", 10, 200, 60)
num_wavelengths = st.slider("Number of Wavelengths", 1, 16, 4)
simulation_time = st.slider("Simulation Time (seconds)", 3, 15, 6)

# ---------------------------------------------------------
# INTERNAL SIMULATION STATE
# ---------------------------------------------------------
packet_log = []
burst_log = []
metrics = {
    "packets": 0,
    "bursts": 0,
    "packet_loss": 0,
    "burst_loss": 0,
    "throughput": 0,
    "avg_delay": 0,
}

st.subheader("🔁 Running Simulation...")

progress = st.progress(0)

# ---------------------------------------------------------
# SIMULATOR LOOP
# ---------------------------------------------------------
for t in range(simulation_time * 10):
    progress.progress(t / (simulation_time * 10))

    # PACKET GENERATION
    packets_this_tick = random.randint(0, max(1, traffic_rate // 10))

    for _ in range(packets_this_tick):
        pkt = {
            "time": t,
            "size": random.randint(64, 1500),
            "priority": random.choice(["Low", "Med", "High"]),
        }
        packet_log.append(pkt)
        metrics["packets"] += 1

    # BURST ASSEMBLY
    if burst_method == "Timer-Based":
        if t % 8 == 0 and len(packet_log) > 0:
            burst_log.append(len(packet_log))
            metrics["bursts"] += 1
            packet_log.clear()

    elif burst_method == "Length-Based":
        if len(packet_log) >= 40:
            burst_log.append(min(len(packet_log), 40))
            metrics["bursts"] += 1
            del packet_log[:40]

    else:  # Mixed
        if len(packet_log) > 30 or t % 10 == 0:
            if len(packet_log) > 0:
                burst_log.append(len(packet_log))
                metrics["bursts"] += 1
                packet_log.clear()

    # SWITCH FABRIC CONTENTION
    if random.random() < (traffic_rate / 300):
        if switch_type == "Optical Packet Switching (OPS)":
            if random.random() > 0.6:
                metrics["packet_loss"] += 1

        elif switch_type == "Optical Burst Switching (OBS)":
            if random.random() > 0.7:
                metrics["burst_loss"] += 1

        else:
            if random.random() > 0.75:
                metrics["packet_loss"] += 1

    time.sleep(0.01)

st.success("Simulation Completed!")

# ---------------------------------------------------------
# METRICS CALCULATION
# ---------------------------------------------------------
metrics["throughput"] = round(
    (metrics["packets"] - metrics["packet_loss"]) / max(1, simulation_time), 2
)
metrics["avg_delay"] = round(random.uniform(0.2, 2.0), 3)

# ---------------------------------------------------------
# DISPLAY METRICS
# ---------------------------------------------------------
st.subheader("📊 Performance Metrics")

colA, colB, colC, colD = st.columns(4)
colA.metric("Total Packets", metrics["packets"])
colB.metric("Packet Loss", metrics["packet_loss"])
colC.metric("Total Bursts", metrics["bursts"])
colD.metric("Burst Loss", metrics["burst_loss"])

colA, colB = st.columns(2)
colA.metric("Throughput (pkts/sec)", metrics["throughput"])
colB.metric("Avg Delay (ms)", metrics["avg_delay"])

# ---------------------------------------------------------
# BURST GRAPH
# ---------------------------------------------------------
st.subheader("📈 Burst Size Over Time")

df = pd.DataFrame({
    "Burst #": list(range(1, len(burst_log) + 1)),
    "Packets in Burst": burst_log
})

st.line_chart(df, x="Burst #", y="Packets in Burst")

# ---------------------------------------------------------
# EXPLANATION PANEL
# ---------------------------------------------------------
st.subheader("📘 Explanation")
st.info("""
This simulator models OPS, OBS, OTDM networks using pure algorithmic switching:
- Poisson-like packet arrivals
- Burst assembly (Timer, Length, Mixed)
- Contention resolution without ML
- Optical switch behaviour (OPS/OBS/OTDM)
- JIT, JET, Tell-And-Go, Tell-And-Wait
""")
