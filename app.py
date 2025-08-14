# app_final_v2.py
# Solar Umbrella Microgrid Simulator (cleaned + extended)
# -------------------------------------------------------
# Purpose:
# - Start on a welcoming "Home" page that explains how this calculator/simulator
#   is the intelligence layer of the Solar Umbrella project.
# - Multi-node ("terrazas") configuration with per-node umbrella type, count,
#   environment factors, self-consumption, EV charging, simple battery model.
# - Hourly EV charging demand simulation (randomized within arrival/departure windows).
# - City selector (CSV optional), umbrella evolution stages (conceptual scaffold).
#
# Notes:
# - If a cities CSV is present, it will be read. Otherwise we fall back to a short list.
# - Keep extending the "Visualize Results" and "Download Report" pages later.

import sys
import os
import json
import base64
from datetime import datetime

# Graceful import for optional internal model (not required to run)
try:
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    from energy_model import distribute_energy  # noqa: F401
except Exception:
    distribute_energy = None

import numpy as np
import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import networkx as nx  # placeholder for future graph visuals
from fpdf import FPDF    # placeholder for future PDF export


# -------------------- Original app_final_v2 Imports and Setup --------------------
# (Paste all original imports, configuration, constants, or helper functions here)

# -------------------- Node and Simulation Setup --------------------
class Node:
    def __init__(self, name, daily_generation, other_params=None):
        self.name = name
        self.daily_generation = daily_generation
        self.hourly_generation = np.zeros(24)  # Initialize hourly generation array
        self.other_params = other_params

nodes = [
    Node('Node 1', 10),
    Node('Node 2', 12),
    Node('Node 3', 9.5)
]

# -------------------- Hourly Generation Function --------------------
def hourly_profile(daily_gen):
    hours = np.arange(24)
    profile = np.sin((hours - 6) / 12 * np.pi) ** 2  # Peaks at midday
    profile = profile / profile.sum()  # Normalize to sum=1
    return daily_gen * profile

# -------------------- Function to Generate Figures --------------------
def get_hourly_generation_figures():
    all_nodes_hourly = [node.hourly_generation for node in nodes]
    # Matplotlib figure
    plt_fig, ax = plt.subplots(figsize=(12,6))
    for i, node_gen in enumerate(all_nodes_hourly):
        ax.plot(range(24), node_gen, label=f'{nodes[i].name}')
    ax.set_xlabel('Hour')
    ax.set_ylabel('Energy Generated (kWh)')
    ax.set_title('Hourly Energy Generation per Node')
    ax.legend()
    ax.grid(True)
    plt.close(plt_fig)

    # Plotly figure
    plotly_fig = go.Figure()
    for i, node_gen in enumerate(all_nodes_hourly):
        plotly_fig.add_trace(go.Scatter(y=node_gen, x=list(range(24)), mode='lines+markers', name=f'{nodes[i].name}'))
    plotly_fig.update_layout(title='Hourly Energy Generation per Node',
                             xaxis_title='Hour',
                             yaxis_title='Energy Generated (kWh)')

    return plt_fig, plotly_fig

# -------------------- Simulation Function --------------------
def run_simulation():
    for node in nodes:
        node.hourly_generation = hourly_profile(node.daily_generation)
    plt_fig, plotly_fig = get_hourly_generation_figures()
    return plt_fig, plotly_fig

# -------------------- Streamlit Main Page --------------------
st.set_page_config(layout="wide")
st.title("Solar Umbrella Simulation")

st.write("Welcome to the Solar Umbrella Simulator! Click the button below to run the simulation and see hourly generation plots.")

if st.button("Run Simulation"):
    plt_fig, plotly_fig = run_simulation()
    col1, col2 = st.columns(2)
    with col1:
        st.pyplot(plt_fig)
    with col2:
        st.plotly_chart(plotly_fig, use_container_width=True)


# -------------------- Simulation Loop --------------------
all_nodes_hourly = []
for node in nodes:
    # Original simulation logic per node goes here

    # Compute hourly generation
    node.hourly_generation = hourly_profile(node.daily_generation)
    all_nodes_hourly.append(node.hourly_generation)


# -------------------------
# Streamlit page config
st.set_page_config(page_title="Solar Umbrella Microgrid", layout="centered")

# -------------------------
# Language + labels

language_map = {
    "English": "en",
    "Español": "es",
}

translations = {
    "en": {
        "choose_language": "🌐 Choose Language",
        "title": "Solar Umbrella Microgrid Simulator",
        "menu": "Menu",
        "home": "Home",
        "configure_run": "Configure & Run",
        "visualize_results": "Visualize Results",
        "download_pdf": "Download Report",
        "location": "🏙️ Choose a city",
        "umbrella": "Umbrella",
        "umbrella_type": "Select Umbrella Type",
        "number_umbrellas": "Number of Umbrellas",
        "season_factor": "Season Factor (0.5 = Winter, 1.0 = Summer)",
        "weather_factor": "Weather Factor (1.0 = Sunny, 0.6 = Cloudy)",
        "temp_efficiency": "Temperature Efficiency Factor",
        "cooling_consumption": "Cooling/Heating (kWh/day per umbrella)",
        "lighting_consumption": "Lighting (kWh/day per umbrella)",
        "operations_consumption": "Operations (kWh/day per umbrella)",
        "number_of_evs": "Number of EVs per Umbrella",
        "avg_kwh_per_ev": "Average kWh per EV per Day",
        "energy_balance": "Umbrella Energy Balance",
        "total_generation": "Total Daily Generation",
        "total_self_consumption": "Total Self-Consumption",
        "total_ev_demand": "Total EV Charging Demand",
        "total_surplus": "Total Surplus",
        "total_deficit": "Total Deficit",
        "node_details": "Node Details",
        "energy_flow_pie_title": "Energy Surplus vs Deficit",
        "surplus_distribution": "Surplus Distribution",
        "adjacent_building": "Adjacent Building",
        "export_grid": "Export to Grid",
        "energy_chart": "Energy Chart",
        "evolution_stage": "Evolution Stage",
        "stage_umbrella": "Umbrella",
        "stage_climate_pod": "Climate Pod",
        "stage_ev_oasis": "EV Oasis / Mobility Node",
        "stage_building_backbone": "Building Energy Backbone",
        "stage_vpp_peer": "Peer in VPP / DER Ecosystem",
        # added/used keys:
        "total_daily_generation": "Total Daily Generation",
        "welcome_title": "Welcome to the Solar Umbrella Project",
        "welcome_body": (
            "This calculator and simulator are the **intelligence layer** of the Solar "
            "Umbrella project. We start with a single solar umbrella that provides shade, "
            "comfort, and clean energy. We then scale to *terrazas* (clusters of umbrellas), "
            "add storage and EV charging, support nearby buildings, and finally interconnect "
            "as peers in distributed energy resources (DER), microgrids, and VPPs."
        ),
        "how_to_use": "How to Use",
        "how_to_steps": (
            "1) Pick your city and language in the sidebar.\n"
            "2) Go to **Configure & Run** to add umbrella nodes, set parameters, and simulate.\n"
            "3) Review the summary results; later you’ll visualize flows and download reports."
        ),
    },
    "es": {
        "choose_language": "🌐 Elige idioma",
        "title": "Simulador de Microred Solar con Sombrillas",
        "menu": "Menú",
        "home": "Inicio",
        "configure_run": "Configurar y Ejecutar",
        "visualize_results": "Visualizar Resultados",
        "download_pdf": "Descargar Informe",
        "location": "🏙️ Elegir Ciudad",
        "umbrella": "Sombrilla",
        "umbrella_type": "Seleccionar Tipo de Sombrilla",
        "number_umbrellas": "Número de Sombrillas",
        "season_factor": "Factor de Temporada (0.5 = Invierno, 1.0 = Verano)",
        "weather_factor": "Factor Climático (1.0 = Soleado, 0.6 = Nublado)",
        "temp_efficiency": "Factor de Eficiencia de Temperatura",
        "cooling_consumption": "Refrigeración/Calefacción (kWh/día por sombrilla)",
        "lighting_consumption": "Iluminación (kWh/día por sombrilla)",
        "operations_consumption": "Operaciones (kWh/día por sombrilla)",
        "number_of_evs": "Número de VEs por Sombrilla",
        "avg_kwh_per_ev": "kWh Promedio por VE por Día",
        "energy_balance": "Balance Energético",
        "total_generation": "Generación Diaria Total",
        "total_self_consumption": "Autoconsumo Total",
        "total_ev_demand": "Demanda de Carga de VE",
        "total_surplus": "Excedente Total",
        "total_deficit": "Déficit Total",
        "node_details": "Detalles del Nodo",
        "energy_flow_pie_title": "Excedente vs Déficit",
        "surplus_distribution": "Distribución del Excedente",
        "adjacent_building": "Edificio Adyacente",
        "export_grid": "Exportar a la Red",
        "energy_chart": "Gráfico de Energía",
        "evolution_stage": "Etapa de Evolución",
        "stage_umbrella": "Sombrilla",
        "stage_climate_pod": "Cápsula Climática",
        "stage_ev_oasis": "Oasis de VE / Nodo de Movilidad",
        "stage_building_backbone": "Espina Dorsal Energética del Edificio",
        "stage_vpp_peer": "Par en VPP / Ecosistema DER",
        # added/used keys:
        "total_daily_generation": "Generación Diaria Total",
        "welcome_title": "Bienvenido al Proyecto Sombrilla Solar",
        "welcome_body": (
            "Este calculador y simulador son la **capa de inteligencia** del proyecto "
            "Sombrilla Solar. Empezamos con una sombrilla que ofrece sombra, confort y "
            "energía limpia. Escalamos a *terrazas* (conjuntos de sombrillas), añadimos "
            "almacenamiento y carga de VE, apoyamos edificios cercanos y finalmente nos "
            "interconectamos como pares en recursos energéticos distribuidos (DER), "
            "microredes y VPP."
        ),
        "how_to_use": "Cómo usar",
        "how_to_steps": (
            "1) Elige tu ciudad e idioma en la barra lateral.\n"
            "2) Ve a **Configurar y Ejecutar** para añadir nodos, ajustar parámetros y simular.\n"
            "3) Revisa el resumen; luego visualizarás flujos y podrás descargar informes."
        ),
    },
}

# -------------------------
# Sidebar: Language
selected_language = st.sidebar.selectbox(
    label=translations["en"]["choose_language"],
    options=list(language_map.keys()),
    key="language_selector",
)
language = language_map.get(selected_language, "en")
labels = translations.get(language, translations["en"])

# -------------------------
# Sidebar: City selector (CSV optional)
st.sidebar.markdown("### " + labels["location"])

# Path hint (Windows path shared by you); will be ignored if not present:
default_city_csv_path = r"C:\Users\Carlos H Betancourth\OneDrive\Documents\GitHub\solar-umbrella-project\data\solar_data.csv"

# Try to load cities from CSV; expect a 'city' column.
cities_from_csv = []
try:
    if os.path.exists(default_city_csv_path):
        df_cities = pd.read_csv(default_city_csv_path)
        if "city" in df_cities.columns:
            cities_from_csv = sorted(df_cities["city"].dropna().unique().tolist())
except Exception:
    cities_from_csv = []

fallback_cities = ["Madrid", "Barcelona", "Bogotá", "Medellín", "Quito", "Lima", "Lisbon", "Rome"]
city_options = cities_from_csv if cities_from_csv else fallback_cities
selected_city = st.sidebar.selectbox("City", city_options, key="city_selector")

# -------------------------
# Umbrella catalog (types & sizes)
# Peak sun hours baseline assumed ~5 h. We want ~14.4 kWh/day for 4x4 in good conditions → ~2.9 kW.
umbrella_types = {
    "3x3 Fixed": {"capacity_kw": 1.8, "notes": "Compact fixed canopy"},
    "4x4 Fixed": {"capacity_kw": 2.9, "notes": "Standard fixed canopy (~14.5 kWh/day @ 5h)"},
    "5x5 Fixed": {"capacity_kw": 4.0, "notes": "Large fixed canopy"},
    "Foldable (Simple)": {"capacity_kw": 3.0, "notes": "Simple fold, sidewalk friendly"},
    "Foldable (Complex)": {"capacity_kw": 3.4, "notes": "Complex fold, better wind/rain handling"},
}

# -------------------------
# Sidebar: Page selection
page = st.sidebar.radio(
    label=labels["menu"],
    options=[labels["home"], labels["configure_run"], labels["visualize_results"], labels["download_pdf"]],
    key="page_selector_unique",
)

# -------------------------
# Home Page
if page == labels["home"]:
    st.title(labels["title"])
    st.subheader(labels["welcome_title"])
    st.write(labels["welcome_body"])
    st.markdown(f"### {labels['how_to_use']}")
    st.write(labels["how_to_steps"])
    st.info(
        "Why umbrellas? In dense cities, rooftops are contested and private parking is scarce. "
        "Cultural umbrellas already sit where people gather (terrazas). They already protect us against heat and rain."  \
        "We evolve them into " "solar generators that protect from heat/rain, power local needs, charge EVs, and "
        "trade energy with nearby loads—growing into a networked VPP."
    )

# -------------------------
# Configure & Run Page
elif page == labels["configure_run"]:
    st.header(labels["configure_run"])
    st.caption(f"City: **{selected_city}**")

    # --- Evolution Stage (conceptual scaffold to tweak defaults as we grow) ---
    stage = st.selectbox(
        labels["evolution_stage"],
        [
            labels["stage_umbrella"],
            labels["stage_climate_pod"],
            labels["stage_ev_oasis"],
            labels["stage_building_backbone"],
            labels["stage_vpp_peer"],
        ],
        key="evolution_stage",
    )

    # --- Global settings (applied across the configured nodes) ---
    st.subheader("Global Settings")
    peak_sun_hours = st.number_input("Peak Sun Hours (baseline)", min_value=1.0, max_value=8.0, value=5.0, step=0.5)

    # This is used in the hourly EV simulation inside each node
    max_charge_power = st.number_input("Max Charging Power per EV (kW)", min_value=1.0, max_value=22.0, value=7.0, step=0.5)

    # Number of nodes (umbrellas clusters/terrazas)
    num_nodes = st.number_input("Number of Umbrella Nodes (Terrazas)", min_value=1, max_value=10, value=3, step=1)

    st.markdown("---")
    st.write("Configure each node:")

    # Storage for node results
    nodes = []

    for i in range(int(num_nodes)):
        st.subheader(f"Umbrella Node #{i+1}")

        # Umbrella
        umbrella_type = st.selectbox(
            f"{labels['umbrella_type']} (Node #{i+1})",
            list(umbrella_types.keys()),
            key=f"umbrella_type_{i}",
        )
        capacity_kw = umbrella_types[umbrella_type]["capacity_kw"]

        num_umbrellas = st.number_input(
            f"{labels['number_umbrellas']} (Node #{i+1})",
            min_value=1, max_value=10, value=1, step=1, key=f"num_umbrellas_{i}"
        )

        # Environment factors
        season_factor = st.slider(
            f"{labels['season_factor']} (Node #{i+1})",
            min_value=0.5, max_value=1.5, value=1.0, step=0.05, key=f"season_factor_{i}"
        )
        weather_factor = st.slider(
            f"{labels['weather_factor']} (Node #{i+1})",
            min_value=0.5, max_value=1.0, value=0.9, step=0.05, key=f"weather_factor_{i}"
        )
        temp_eff_factor = st.slider(
            f"{labels['temp_efficiency']} (Node #{i+1})",
            min_value=0.8, max_value=1.0, value=0.95, step=0.01, key=f"temp_eff_factor_{i}"
        )

        # Self consumption (per umbrella)
        cooling_cons = st.number_input(
            f"{labels['cooling_consumption']} (Node #{i+1})", min_value=0.0, max_value=10.0, value=2.5, step=0.1,
            key=f"cool_{i}"
        )
        lighting_cons = st.number_input(
            f"{labels['lighting_consumption']} (Node #{i+1})", min_value=0.0, max_value=5.0, value=0.5, step=0.1,
            key=f"light_{i}"
        )
        ops_cons = st.number_input(
            f"{labels['operations_consumption']} (Node #{i+1})", min_value=0.0, max_value=5.0, value=0.3, step=0.1,
            key=f"ops_{i}"
        )

        # Battery
        battery_capacity = st.number_input(
            f"Battery Capacity (kWh) (Node #{i+1})", min_value=0.0, max_value=200.0, value=10.0, step=0.5,
            key=f"bat_cap_{i}"
        )
        battery_charge_eff = st.slider(
            f"Battery Charge Efficiency (Node #{i+1})", min_value=0.7, max_value=1.0, value=0.9, step=0.01,
            key=f"bat_ch_eff_{i}"
        )
        battery_discharge_eff = st.slider(
            f"Battery Discharge Efficiency (Node #{i+1})", min_value=0.7, max_value=1.0, value=0.9, step=0.01,
            key=f"bat_dis_eff_{i}"
        )
        battery_max_charge = st.number_input(
            f"Max Battery Charge Rate (kW) (Node #{i+1})", min_value=0.1, max_value=50.0, value=5.0, step=0.1,
            key=f"bat_max_ch_{i}"
        )
        battery_max_discharge = st.number_input(
            f"Max Battery Discharge Rate (kW) (Node #{i+1})", min_value=0.1, max_value=50.0, value=5.0, step=0.1,
            key=f"bat_max_dis_{i}"
        )

        # EV demand parameters (per umbrella)
        num_evs = st.number_input(
            f"{labels['number_of_evs']} (Node #{i+1})", min_value=0, max_value=10, value=1, step=1, key=f"num_evs_{i}"
        )
        avg_kwh_per_ev = st.number_input(
            f"{labels['avg_kwh_per_ev']} (Node #{i+1})", min_value=0.0, max_value=100.0, value=8.0, step=0.5,
            key=f"avg_ev_{i}"
        )

        # --- Energy generation per node (daily) ---
        daily_energy_kwh_per_umbrella = capacity_kw * peak_sun_hours * season_factor * weather_factor * temp_eff_factor
        total_daily_generation = daily_energy_kwh_per_umbrella * num_umbrellas

        # --- Self-consumption per node (daily) ---
        total_self_consumption = (cooling_cons + lighting_cons + ops_cons) * num_umbrellas

        # --- Hourly EV charging demand simulation (per node) ---
        # Windows for arrival/departure; tweak later by stage if desired
        arrival_start, arrival_end = 8, 10    # 8–10 AM
        departure_start, departure_end = 17, 20  # 5–8 PM
        hours = 24
        ev_charging_profiles = []

        for ev in range(int(num_evs)):
            arrival_time = np.random.randint(arrival_start, arrival_end + 1)
            departure_time = np.random.randint(departure_start, departure_end + 1)
            if departure_time <= arrival_time:
                departure_time = arrival_time + 1
            charging_hours = max(1, departure_time - arrival_time)
            # Energy per EV per hour (capped by charger power)
            energy_per_hour = min(avg_kwh_per_ev / charging_hours, max_charge_power)
            ev_load = np.zeros(hours)
            ev_load[arrival_time:departure_time] = energy_per_hour
            ev_charging_profiles.append(ev_load)

        hourly_ev_demand = np.sum(ev_charging_profiles, axis=0) if ev_charging_profiles else np.zeros(hours)
        total_ev_demand = hourly_ev_demand.sum() * num_umbrellas  # daily EV energy per node

        # --- Simple daily battery operation (scalar) ---
        net_energy = total_daily_generation - total_self_consumption - total_ev_demand
        battery_soc = 0.5 * battery_capacity  # start SoC (kWh)

        if net_energy > 0:
            # Charge with surplus (limited by charge rate & capacity)
            charge_power = min(net_energy, battery_max_charge)
            charge_energy = charge_power * battery_charge_eff
            battery_soc = min(battery_capacity, battery_soc + charge_energy)
            surplus_energy = max(0.0, net_energy - charge_power)
            deficit_energy = 0.0
        else:
            # Discharge to cover deficit (limited by discharge rate & SoC)
            needed = abs(net_energy)
            discharge_power = min(needed, battery_max_discharge, battery_soc)
            discharge_energy = discharge_power / max(1e-6, battery_discharge_eff)
            battery_soc = max(0.0, battery_soc - discharge_energy)
            surplus_energy = 0.0
            deficit_energy = max(0.0, needed - discharge_power)

        # Store per-node results
        node = {
            "node_id": i + 1,
            "city": selected_city,
            "stage": stage,
            "umbrella_type": umbrella_type,
            "num_umbrellas": int(num_umbrellas),
            "daily_generation": float(total_daily_generation),
            "self_consumption": float(total_self_consumption),
            "ev_demand": float(total_ev_demand),
            "battery_capacity": float(battery_capacity),
            "battery_soc_end": float(battery_soc),
            "surplus": float(surplus_energy),
            "deficit": float(deficit_energy),
            # keep hourly for future plots
            "hourly_ev_demand": hourly_ev_demand.tolist(),
        }
        nodes.append(node)

    # --- Aggregate results across nodes ---
    total_generation_all = sum(n["daily_generation"] for n in nodes)
    total_self_cons_all = sum(n["self_consumption"] for n in nodes)
    total_ev_demand_all = sum(n["ev_demand"] for n in nodes)
    total_surplus_all = sum(n["surplus"] for n in nodes)
    total_deficit_all = sum(n["deficit"] for n in nodes)
    avg_battery_soc = (sum(n["battery_soc_end"] for n in nodes) / len(nodes)) if nodes else 0.0

    st.markdown("## Microgrid Summary")
    st.write(f"{labels['total_generation']}: **{total_generation_all:.2f} kWh/day**")
    st.write(f"{labels['total_self_consumption']}: **{total_self_cons_all:.2f} kWh/day**")
    st.write(f"{labels['total_ev_demand']}: **{total_ev_demand_all:.2f} kWh/day**")
    st.write(f"{labels['total_surplus']}: **{total_surplus_all:.2f} kWh/day**")
    st.write(f"{labels['total_deficit']}: **{total_deficit_all:.2f} kWh/day**")
    st.write(f"Average Battery SoC (end of day): **{avg_battery_soc:.2f} kWh**")

    # Pie chart: Surplus vs Deficit
    surplus_vs_deficit = pd.DataFrame({
        "Energy Type": [labels["total_surplus"], labels["total_deficit"]],
        "Energy (kWh)": [total_surplus_all, total_deficit_all],
    })
    fig = px.pie(surplus_vs_deficit, values="Energy (kWh)", names="Energy Type",
                 title=labels["energy_flow_pie_title"])
    st.plotly_chart(fig, use_container_width=True)

    # Node table
    st.markdown("### " + labels["node_details"])
    df_nodes = pd.DataFrame(nodes)
    st.dataframe(df_nodes, use_container_width=True)

# -------------------------
# Visualize Results Page (placeholder for next steps)
elif page == labels["visualize_results"]:
    st.header(labels["visualize_results"])
    st.write("Visualizations will be here soon — hourly charts, microgrid flows, and network graphs.")

# -------------------------
# Download Report Page (placeholder for next steps)
elif page == labels["download_pdf"]:
    st.header(labels["download_pdf"])
    st.write("Report generation coming soon...")
