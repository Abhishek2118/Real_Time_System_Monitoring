import psutil
import streamlit as st
import time
import plotly.graph_objects as go

# Store historical data
cpu_usage = []
mem_usage = []
disk_usage = []
network_sent = []
network_recv = []

def get_metrics():
    return {
        "CPU Usage": psutil.cpu_percent(),
        "Memory Usage": psutil.virtual_memory().percent,
        "Disk Usage": psutil.disk_usage('/').percent,
        "Network Sent": psutil.net_io_counters().bytes_sent / 1024,
        "Network Received": psutil.net_io_counters().bytes_recv / 1024
    }

st.title("Advanced Real-Time System Monitor")
st.sidebar.header("Monitoring Settings")
refresh_rate = st.sidebar.slider("Refresh Rate (seconds)", 1, 10, 1)
max_data_points = st.sidebar.slider("Max Data Points", 10, 100, 50)

placeholder = st.empty()

while True:
    metrics = get_metrics()
    
    cpu_usage.append(metrics["CPU Usage"])
    mem_usage.append(metrics["Memory Usage"])
    disk_usage.append(metrics["Disk Usage"])
    network_sent.append(metrics["Network Sent"])
    network_recv.append(metrics["Network Received"])
    
    # Maintain list size
    if len(cpu_usage) > max_data_points:
        cpu_usage.pop(0)
        mem_usage.pop(0)
        disk_usage.pop(0)
        network_sent.pop(0)
        network_recv.pop(0)
    
    with placeholder.container():
        st.subheader("Current System Metrics")
        st.write(f"**CPU Usage:** {metrics['CPU Usage']}%")
        st.write(f"**Memory Usage:** {metrics['Memory Usage']}%")
        st.write(f"**Disk Usage:** {metrics['Disk Usage']}%")
        st.write(f"**Network Sent:** {metrics['Network Sent']:.2f} KB")
        st.write(f"**Network Received:** {metrics['Network Received']:.2f} KB")
        
        st.subheader("Performance Trends")
        
        fig_cpu = go.Figure([go.Scatter(y=cpu_usage, mode='lines', name='CPU Usage')])
        fig_mem = go.Figure([go.Scatter(y=mem_usage, mode='lines', name='Memory Usage')])
        fig_disk = go.Figure([go.Scatter(y=disk_usage, mode='lines', name='Disk Usage')])
        fig_net = go.Figure([
            go.Scatter(y=network_sent, mode='lines', name='Network Sent'),
            go.Scatter(y=network_recv, mode='lines', name='Network Received')
        ])
        
        st.plotly_chart(fig_cpu)
        st.plotly_chart(fig_mem)
        st.plotly_chart(fig_disk)
        st.plotly_chart(fig_net)
    
    time.sleep(refresh_rate)
