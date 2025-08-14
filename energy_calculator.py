import streamlit as st
import plotly.graph_objects as go
import json
import pandas as pd

from datetime import datetime
def calculate_energy_output(width, length, coverage_efficiency, panel_efficiency, solar_irradiance, system_losses):
    surface_area_m2 = width * length * coverage_efficiency
    daily_energy_output_kWh = surface_area_m2 * panel_efficiency * solar_irradiance * system_losses
    return round(daily_energy_output_kWh, 2)

def calculate_co2_savings(kwh, emission_factor):
    return round(kwh * emission_factor, 2)

def calculate_cost_savings(kwh, price_per_kwh):
    return round(kwh * price_per_kwh, 2)

def calculate_battery_backup(daily_output, battery_capacity, efficiency, days_autonomy):
    usable_capacity = battery_capacity * efficiency
    backup_days = round(usable_capacity / daily_output, 2) if daily_output else 0
    meets_autonomy = backup_days >= days_autonomy
    return usable_capacity, backup_days, meets_autonomy


# --- Page Config ---
st.set_page_config(page_title="Solar System Calculator", layout="centered")
st.title("🔆 Solar Energy Output & Storage Calculator")

# --- System Type Toggle ---
system_type = st.radio("System Type", ["Umbrella", "Rooftop"])

# --- Sidebar Inputs ---
st.sidebar.header(f"{system_type} Parameters")
width = st.sidebar.slider(f"{system_type} Width (m)", 2.0, 10.0, 4.0)
length = st.sidebar.slider(f"{system_type} Length (m)", 2.0, 10.0, 4.0)
coverage_efficiency = st.sidebar.slider("Panel Coverage Efficiency", 0.5, 1.0, 0.85)
panel_efficiency = st.sidebar.slider("Panel Efficiency", 0.10, 0.25, 0.20)
system_losses = st.sidebar.slider("System Efficiency After Losses", 0.6, 1.0, 0.85)
num_units = st.sidebar.slider(f"Number of {system_type}s", 1, 10, 1)

# --- Location-based Irradiance & CO₂ Factors ---
location = st.sidebar.selectbox("Location", ["Custom", "Barcelona", "Madrid", "Málaga", "Sevilla", "Amsterdam", "Paris", "Berlin", "Nairobi", "Tokyo", "Los Angeles"])
irradiance_map = {
    "Barcelona": 5.0,
    "Madrid": 5.2,
    "Málaga": 5.5,
    "Sevilla": 5.6,
    "Amsterdam": 3.2,
    "Paris": 3.5,
    "Berlin": 3.8,
    "Nairobi": 5.5,
    "Tokyo": 4.2,
    "Los Angeles": 5.8
}
co2_map = {
    "Barcelona": 0.25,
    "Madrid": 0.23,
    "Málaga": 0.24,
    "Sevilla": 0.24,
    "Amsterdam": 0.35,
    "Paris": 0.30,
    "Berlin": 0.32,
    "Nairobi": 0.15,
    "Tokyo": 0.35,
    "Los Angeles": 0.40
}

if location == "Custom":
    solar_irradiance = st.sidebar.slider("Solar Irradiance (kWh/m²/day)", 3.0, 7.0, 5.0)
    co2_factor = st.sidebar.slider("CO₂ Emission Factor (kg/kWh)", 0.1, 0.6, 0.4)
else:
    solar_irradiance = irradiance_map[location]
    co2_factor = co2_map[location]
    st.sidebar.write(f"Using irradiance for {location}: {solar_irradiance} kWh/m²/day")
    st.sidebar.write(f"Using CO₂ factor for {location}: {co2_factor} kg/kWh")

# --- Electricity Price ---
price_per_kwh = st.sidebar.slider("Electricity Price (€/kWh)", 0.05, 0.50, 0.25)

# --- Battery Inputs ---
st.sidebar.header("🔋 Battery Storage")
battery_capacity = st.sidebar.slider("Battery Capacity (kWh)", 1.0, 50.0, 10.0)
battery_efficiency = st.sidebar.slider("Battery Efficiency (%)", 0.6, 1.0, 0.9)
days_autonomy = st.sidebar.slider("Required Days of Autonomy", 1, 7, 2)

# --- Calculations ---
energy_output_per = calculate_energy_output(width, length, coverage_efficiency, panel_efficiency, solar_irradiance, system_losses)
total_output = round(energy_output_per * num_units, 2)

monthly_output = round(total_output * 30, 2)
yearly_output = round(total_output * 365, 2)

daily_co2 = calculate_co2_savings(total_output, co2_factor)
monthly_co2 = calculate_co2_savings(monthly_output, co2_factor)
yearly_co2 = calculate_co2_savings(yearly_output, co2_factor)

daily_savings = calculate_cost_savings(total_output, price_per_kwh)
monthly_savings = calculate_cost_savings(monthly_output, price_per_kwh)
yearly_savings = calculate_cost_savings(yearly_output, price_per_kwh)

usable_capacity, backup_days, meets_autonomy = calculate_battery_backup(total_output, battery_capacity, battery_efficiency, days_autonomy)

# --- Display Results ---
st.subheader("🔋 Estimated Energy Output")
st.write(f"**Per {system_type}:** {energy_output_per} kWh/day")
st.write(f"**Total for {num_units} {system_type}(s):** {total_output} kWh/day")

st.subheader("📅 Projections")
st.write(f"**Monthly Output:** {monthly_output} kWh")
st.write(f"**Yearly Output:** {yearly_output} kWh")

st.subheader("🌱 CO₂ Emissions Avoided")
st.write(f"**Daily:** {daily_co2} kg")
st.write(f"**Monthly:** {monthly_co2} kg")
st.write(f"**Yearly:** {yearly_co2} kg")

st.subheader("💰 Estimated Cost Savings")
st.write(f"**Daily:** €{daily_savings}")
st.write(f"**Monthly:** €{monthly_savings}")
st.write(f"**Yearly:** €{yearly_savings}")

st.subheader("🔋 Battery Storage Analysis")
st.write(f"**Usable Battery Capacity:** {usable_capacity} kWh")
st.write(f"**Estimated Backup Duration:** {backup_days} day(s)")
st.write(f"**Meets Autonomy Requirement:** {'✅ Yes' if meets_autonomy else '❌ No'}")

# --- Interactive Chart ---
unit_counts = list(range(1, 11))
outputs = [
    calculate_energy_output(
        width, length, coverage_efficiency,
        panel_efficiency, solar_irradiance, system_losses
    ) * n for n in unit_counts
]

fig = go.Figure()
fig.add_trace(go.Scatter(
    x=unit_counts,
    y=outputs,
    mode='lines+markers',
    marker=dict(color='orange'),
    name='Energy Output',
    hovertemplate=f'{system_type}s: %{{x}}<br>Energy: %{{y:.2f}} kWh/day'
))
fig.update_layout(
    title=f"📈 Energy Output vs. {system_type} Count",
    xaxis_title=f"Number of {system_type}s",
    yaxis_title="Total Energy Output (kWh/day)",
    template="plotly_white"
)
st.plotly_chart(fig)

# --- Target Comparison ---
target_kwh = st.number_input("🎯 Target Daily Energy (kWh)", value=14.4)
units_needed = round(target_kwh / energy_output_per, 1) if energy_output_per else 0
st.write(f"To meet **{target_kwh} kWh/day**, you need approximately **{units_needed} {system_type}(s)**.")

# --- Export Configuration ---
config = {
    "timestamp": datetime.now().isoformat(),
    "system_type": system_type,
    "location": location,
    "width": width,
    "length": length,
    "coverage_efficiency": coverage_efficiency,
    "panel_efficiency": panel_efficiency,
    "solar_irradiance": solar_irradiance,
    "system_losses": system_losses,
    "num_units": num_units,
    "energy_output_per": energy_output_per,
    "total_output": total_output,
    "monthly_output": monthly_output,
    "yearly_output": yearly_output,
    "co2_factor": co2_factor,
    "daily_co2": daily_co2,
    "monthly_co2": monthly_co2,
    "yearly_co2": yearly_co2,
    "price_per_kwh": price_per_kwh,
    "daily_savings": daily_savings,
    "monthly_savings": monthly_savings,
    "yearly_savings": yearly_savings,
    "battery_capacity": battery_capacity,
    "battery_efficiency": battery_efficiency,
    "days_autonomy": days_autonomy,
    "usable_capacity": usable_capacity,
    "backup_days": backup_days,
    "meets_autonomy": meets_autonomy,
    "target_kwh": target_kwh,
    "units_needed": units_needed
}
# --- JSON Export ---
st.download_button("📥 Download Configuration (JSON)", data=json.dumps(config, indent=2), file_name="solar_config.json")

# --- CSV Export ---
df = pd.DataFrame([config])
csv_data = df.to_csv(index=False)
st.download_button(
    label="📥 Download Configuration (CSV)",
    data=csv_data,
    file_name="solar_config.csv",
    mime="text/csv"
)
