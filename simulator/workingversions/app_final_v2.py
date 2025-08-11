import streamlit as st
import json
import pandas as pd
from energy_model import distribute_energy
from fpdf import FPDF
import base64
from io import BytesIO
from datetime import datetime
import matplotlib.pyplot as plt
import plotly.express as px
import networkx as nx

def generate_simulator_url(payload: dict) -> str:
    payload_json = json.dumps(payload, indent=2)
    encoded_payload = base64.b64encode(payload_json.encode()).decode()
    return f"https://app-pdf-app-6dspduazqvsgwpnvfvcbds.streamlit.app/?data={encoded_payload}"

# 🔽 Language mapping for user-friendly labels
language_map = {
    "English": "en",
    "Español": "es",
    "Nederlands": "nl",
    "Català": "ca"
}

# 🌐 Language translations
translations = {
    "en": {
        "title": "Solar Umbrella Microgrid Simulator",
        "run_test": "Run Test",
        "visualize_results": "Visualize Results",
        "download_pdf": "Download PDF",
        "home": "Home",
        "upload_layout": "Upload layout JSON",
        "export_layout": "Export Current Layout",
        "sunlight_hours": "Sunlight Hours",
        "num_nodes": "Number of Solar Umbrella Nodes",
        "node_settings": "Node Settings",
        "usage_factor": "Usage Factor",
        "umbrella": "Umbrella Type",
        "role": "Role",
        "configured_nodes": "Configured Nodes",
        "run_simulation": "Run Simulation",
        "simulation_completed": "Simulation completed!",
        "results": "Results",
        "generated": "Generated",
        "demand": "Demand",
        "surplus": "Surplus",
        "battery_storage": "Battery Stored",
        "co2_emission": "CO₂ Emissions",
        "summary_stats": "Summary Stats",
        "total_generated": "Total Generated",
        "total_demand": "Total Demand",
        "average_surplus": "Average Surplus",
        "base_vs_surplus": "Base Energy vs Surplus",
        "energy_chart": "Energy Overview Chart",
        "node_summary": "Node Energy Summary",
        "simulation_history": "Simulation History",
        "download_report": "Download your report below.",
        "pdf_ready": "PDF generation is ready!",
        "run_first": "Please run the simulation first.",
        "logo_missing": "Logo not found. You can add one at: "
    },
    "es": {
        "title": "Simulador de Microred Solar con Sombrillas",
        "run_test": "Ejecutar Prueba",
        "visualize_results": "Visualizar Resultados",
        "download_pdf": "Descargar PDF",
        "home": "Inicio",
        "upload_layout": "Subir diseño JSON",
        "export_layout": "Exportar Diseño Actual",
        "sunlight_hours": "Horas de Sol",
        "num_nodes": "Número de Nodos",
        "node_settings": "Configuración del Nodo",
        "usage_factor": "Factor de Uso",
        "umbrella": "Tipo de Sombrilla",
        "role": "Rol",
        "configured_nodes": "Nodos Configurados",
        "run_simulation": "Ejecutar Simulación",
        "simulation_completed": "¡Simulación completada!",
        "results": "Resultados",
        "generated": "Generado",
        "demand": "Demanda",
        "surplus": "Excedente",
        "battery_storage": "Almacenamiento en Batería",
        "co2_emission": "Emisiones de CO₂",
        "summary_stats": "Estadísticas Resumen",
        "total_generated": "Total Generado",
        "total_demand": "Demanda Total",
        "average_surplus": "Excedente Promedio",
        "base_vs_surplus": "Energía Base vs Excedente",
        "energy_chart": "Gráfico de Energía",
        "node_summary": "Resumen de Energía por Nodo",
        "simulation_history": "Historial de Simulaciones",
        "download_report": "Descarga tu informe abajo.",
        "pdf_ready": "¡PDF listo para descargar!",
        "run_first": "Ejecuta la simulación primero.",
        "logo_missing": "Logo no encontrado. Puedes añadir uno en: "
    },
    "nl": {
        "title": "Simulator voor Zonneparaplu Microgrid",
        "run_test": "Test Uitvoeren",
        "visualize_results": "Resultaten Bekijken",
        "download_pdf": "PDF Downloaden",
        "home": "Startpagina",
        "upload_layout": "Layout JSON Uploaden",
        "export_layout": "Huidige Layout Exporteren",
        "sunlight_hours": "Zonuren",
        "num_nodes": "Aantal Zonneparaplu Nodes",
        "node_settings": "Node-instellingen",
        "usage_factor": "Gebruik Factor",
        "umbrella": "Paraplu Type",
        "role": "Rol",
        "configured_nodes": "Geconfigureerde Nodes",
        "run_simulation": "Simulatie Uitvoeren",
        "simulation_completed": "Simulatie voltooid!",
        "results": "Resultaten",
        "generated": "Opgewekt",
        "demand": "Vraag",
        "surplus": "Overschot",
        "battery_storage": "Batterijopslag",
        "co2_emission": "CO₂-uitstoot",
        "summary_stats": "Samenvattingsstatistieken",
        "total_generated": "Totaal Opgewekt",
        "total_demand": "Totale Vraag",
        "average_surplus": "Gemiddeld Overschot",
        "base_vs_surplus": "Basisenergie vs Overschot",
        "energy_chart": "Energieoverzicht",
        "node_summary": "Node Energieoverzicht",
        "simulation_history": "Simulatiegeschiedenis",
        "download_report": "Download je rapport hieronder.",
        "pdf_ready": "PDF is klaar!",
        "run_first": "Voer eerst de simulatie uit.",
        "logo_missing": "Logo niet gevonden. Voeg er een toe op: "
    },
    "ca": {
        "title": "Simulador de Microxarxa Solar amb Para-sols",
        "run_test": "Executar Prova",
        "visualize_results": "Visualitzar Resultats",
        "download_pdf": "Descarregar PDF",
        "home": "Inici",
        "upload_layout": "Pujar disseny JSON",
        "export_layout": "Exportar Disseny Actual",
        "sunlight_hours": "Hores de Sol",
        "num_nodes": "Nombre de Nodes",
        "node_settings": "Configuració del Node",
        "usage_factor": "Factor d'Ús",
        "umbrella": "Tipus de Para-sol",
        "role": "Rol",
        "configured_nodes": "Nodes Configurats",
        "run_simulation": "Executar Simulació",
        "simulation_completed": "Simulació completada!",
        "results": "Resultats",
        "generated": "Generat",
        "demand": "Demanda",
        "surplus": "Excés",
        "battery_storage": "Emmagatzematge de Bateria",
        "co2_emission": "Emissions de CO₂",
        "summary_stats": "Estadístiques Resum",
        "total_generated": "Total Generat",
        "total_demand": "Demanda Total",
        "average_surplus": "Excés Mitjà",
        "base_vs_surplus": "Energia Base vs Excés",
        "energy_chart": "Gràfic d'Energia",
        "node_summary": "Resum d'Energia per Node",
        "simulation_history": "Historial de Simulacions",
        "download_report": "Descarrega el teu informe a sota.",
        "pdf_ready": "PDF llest!",
        "run_first": "Executa la simulació primer.",
        "logo_missing": "Logo no trobat. Pots afegir-ne un a: "
    }
}

# ✅ Then use it in the selector

selected_language = st.sidebar.selectbox("🌐 Choose Language", list(language_map.keys()), key="language_selector")

language = language_map[selected_language]
labels = translations[language]

# ✅ Now it's safe to use labels
st.title("🌞 " + labels["title"])



# 🌐 Logo placeholder
st.image("https://via.placeholder.com/150?text=Logo", width=150)


# 📊 Load city data
import pandas as pd

df = pd.read_csv("solar_microgrid_sim/data/solar_data.csv")
cities = sorted(df["city"].unique())
selected_city = st.selectbox("🏙️ Choose a city", cities)



# 🌞 Title and description
st.title("🌞 " + labels["title"])
st.caption("Simulate, visualize, and export solar microgrid performance with advanced features.")

# 🌐 Language selector

language = language_map[selected_language]

labels = translations[language]

# 🖼️ Logo or banner — move to sidebar
st.sidebar.image("https://via.placeholder.com/150?text=Logo", use_container_width=True)

# 🧭 Sidebar navigation
page = st.sidebar.radio(
    labels["title"],
    [labels["home"], labels["run_test"], labels["visualize_results"], labels["download_pdf"]],
    key="page_selector"
)

# 🔑 Access your weather API key from secrets.toml
weather_api_key = st.secrets["general"]["weather_api_key"]

# ✅ Check if the API key is loaded correctly
if weather_api_key:
    st.success("✅ API key is loaded.")
else:
    st.error("❌ API key not found.")


language_code = language_map.get(selected_language, "en")
labels = translations.get(language_code, translations["en"])

# ✅ Now you can use `labels` throughout your app

def get_sidebar_inputs(labels):
    sunlight_hours = st.sidebar.slider("☀️ " + labels["sunlight_hours"], 0, 12, 6)
    st.session_state.sunlight_hours = sunlight_hours
    num_nodes = st.sidebar.slider("🌞 " + labels["num_nodes"], 1, 10, 4)
    return sunlight_hours, num_nodes

def configure_nodes(num_nodes, sunlight_hours, labels):
    umbrella_options = ["Standard", "Reflective", "Smart"]
    role_options = ["Producer", "Consumer", "Hybrid"]
    nodes = []

    for i in range(num_nodes):
        node_id = f"Node {i+1}"
        st.sidebar.subheader(f"⚙️ {node_id} {labels['node_settings']}")
        usage_factor = st.sidebar.slider(f"{node_id} {labels['usage_factor']}", 0.5, 2.0, 1.0)
        umbrella = st.sidebar.selectbox(f"{node_id} {labels['umbrella']}", umbrella_options, key=f"umbrella_{i}")
        role = st.sidebar.selectbox(f"{node_id} {labels['role']}", role_options, key=f"role_{i}")

        node = {
            "id": node_id,
            "usage_factor": usage_factor,
            "base_energy": sunlight_hours * 1.5,
            "umbrella": umbrella,
            "role": role,
            "battery_capacity": 5.0
        }
        nodes.append(node)

    return nodes

def run_simulation(nodes, sunlight_hours):
    results = distribute_energy(nodes, sunlight_hours)
    st.session_state.results = results

    summary = {
        "Run": datetime.now().strftime("%H:%M:%S"),
        "Total Generated": sum([n["generated"] for n in results.values()]),
        "Total Demand": sum([n["demand"] for n in results.values()]),
        "Average Surplus": sum([n["surplus"] for n in results.values()]) / len(results)
    }

    if "history" not in st.session_state:
        st.session_state.history = []

    st.session_state.history.append(summary)
    return results, summary

def build_simulator_payload(location, sunlight_hours, nodes, summary):
    payload = {
        "location": location,
        "sunlight_hours": sunlight_hours,
        "num_nodes": len(nodes),
        "nodes": nodes,
        "summary": summary,
        "timestamp": datetime.now().isoformat()
    }
    return payload

# 🌍 Choose language

# 📍 Location input
location = st.text_input("📍 " + labels.get("location", "Location"), "Barcelona")
# 🎛️ Sidebar inputs
sunlight_hours, num_nodes = get_sidebar_inputs(labels)

# 🧩 Node configuration
nodes = configure_nodes(num_nodes, sunlight_hours, labels)

# 🚀 Run simulation
if st.button("▶️ " + labels["run_simulation"]):
    results, summary = run_simulation(nodes, sunlight_hours)
    st.success("✅ " + labels["simulation_completed"])

    # 📊 Display results
    st.subheader("📊 " + labels["results"])
    for node_id, data in results.items():
        st.write(f"**{node_id}**")
        st.write(f"- Generated: {data['generated']} kWh")
        st.write(f"- Demand: {data['demand']} kWh")
        st.write(f"- Surplus: {data['surplus']} kWh")
        st.write("---")

    # 📦 Payload preview
    payload = build_simulator_payload(location, sunlight_hours, nodes, summary)
    st.json(payload)


# 🔧 Page setup
st.set_page_config(page_title="Solar Umbrella Microgrid", layout="centered")



# 🏷️ Main page title and caption
st.title("🌞 " + labels["title"])
st.caption("Simulate, visualize, and export solar microgrid performance with advanced features.")


st.image("https://via.placeholder.com/150?text=Logo", use_container_width=True)

st.title("🌞 " + labels["title"])
st.caption("Simulate, visualize, and export solar microgrid performance with advanced features.")


# 📤 Upload layout
uploaded_file = st.sidebar.file_uploader("📤 " + labels["upload_layout"], type="json")
try:
    if uploaded_file:
        layout = json.load(uploaded_file)
        st.success("✅ Custom layout loaded")
    else:
        with open("solar_microgrid_sim/data/sample_layout.json") as f:
            layout = json.load(f)
        st.info("ℹ️ Using default layout")
except Exception as e:
    st.error(f"❌ Error loading layout: {e}")
    layout = {}

# 🏠 Home Page
if page == labels["home"]:
    st.write("Welcome to the Solar Microgrid Simulator!")
    if layout:
        st.download_button("📁 " + labels["export_layout"], json.dumps(layout, indent=2), file_name="layout_export.json")

# 🧪 Run Test Page
elif page == labels["run_test"]:
    from datetime import datetime
    import json
    import base64

    # 🌞 Sidebar inputs
    st.sidebar.header(labels["node_settings"])
    sunlight_hours = st.sidebar.slider("☀️ " + labels["sunlight_hours"], 0, 12, 6, key="sunlight_slider")
    st.session_state.sunlight_hours = sunlight_hours

    # 🌞 Main area inputs
    num_nodes = st.slider("🌞 " + labels["num_nodes"], 1, 10, 4, key="num_nodes_slider")
    umbrella_options = ["Standard", "Reflective", "Smart"]
    role_options = ["Producer", "Consumer", "Hybrid"]

    # 🟢 First button: Configure nodes
    if st.button("▶️ " + labels["run_simulation"], key="run_test_simulation_button"):
        # 🔧 Logic to run when button is clicked
        st.success("Simulation started with:")
        st.write(f"☀️ Sunlight Hours: {sunlight_hours}")
        st.write(f"🌞 Number of Nodes: {num_nodes}")
        st.write(f"🌂 Umbrella Options: {umbrella_options}")
        st.write(f"🔌 Role Options: {role_options}")
        # You can call your simulation function here
        # run_simulation(sunlight_hours, num_nodes, umbrella_options, role_options)
if st.button("Run Simulation"):
    nodes = []
    for i in range(num_nodes):
        node_id = f"Node {i+1}"
        st.sidebar.subheader(f"⚙️ {node_id} {labels['node_settings']}")
        usage_factor = st.sidebar.slider(f"{node_id} {labels['usage_factor']}", 0.5, 2.0, 1.0)
        umbrella = st.sidebar.selectbox(f"{node_id} {labels['umbrella']}", umbrella_options, key=f"umbrella_{i}")
        role = st.sidebar.selectbox(f"{node_id} {labels['role']}", role_options, key=f"role_{i}")

        node = {
            "id": node_id,
            "usage_factor": usage_factor,
            "base_energy": sunlight_hours * 1.5,
            "umbrella": umbrella,
            "role": role,
            "battery_capacity": 5.0
        }
        nodes.append(node)

    st.session_state.nodes = nodes
    st.success("✅ Nodes configured successfully!")

# 🟡 Show configured nodes
if "nodes" in st.session_state:
    st.write("🔌 " + labels["configured_nodes"], st.session_state.nodes)

# 🔵 Second button: Run actual simulation
if st.button(labels["run_simulation"], key="run_simulation_button"):
    nodes = st.session_state.get("nodes", [])
    if nodes:
        results = distribute_energy(nodes, sunlight_hours)
        st.session_state.results = results

        summary = {
            "Run": datetime.now().strftime("%H:%M:%S"),
            "Total Generated": sum([n["generated"] for n in results.values()]),
            "Total Demand": sum([n["demand"] for n in results.values()]),
            "Average Surplus": sum([n["surplus"] for n in results.values()]) / len(results)
        }

        if "history" not in st.session_state:
            st.session_state.history = []

        st.session_state.history.append(summary)

        st.success("✅ " + labels["simulation_completed"])
        st.write("📊 " + labels["results"])
        st.json(results)
    else:
        st.error("⚠️ Please configure nodes first by clicking 'Run Simulation'.")

    # ✅ Payload and simulator button
    simulator_payload = {
        "location": st.session_state.get("location", "Custom"),
        "sunlight_hours": sunlight_hours,
        "num_nodes": num_nodes,
        "nodes": nodes,
        "summary": summary,
        "timestamp": datetime.now().isoformat()
    }

    simulator_url = generate_simulator_url(simulator_payload)

    if st.button("🚀 Send to Simulator", key="send_to_simulator"):
        st.markdown(f"[Click here to open Simulator with data]({simulator_url})", unsafe_allow_html=True)

from datetime import datetime
import json
import base64

# ✅ Only build and send payload if results exist
if "results" in st.session_state and "nodes" in st.session_state and "sunlight_hours" in st.session_state:
    results = st.session_state.results
    nodes = st.session_state.nodes
    sunlight_hours = st.session_state.sunlight_hours

    summary = {
        "Run": datetime.now().strftime("%H:%M:%S"),
        "Total Generated": sum([n["generated"] for n in results.values()]),
        "Total Demand": sum([n["demand"] for n in results.values()]),
        "Average Surplus": sum([n["surplus"] for n in results.values()]) / len(results)
    }

    if "history" not in st.session_state:
        st.session_state.history = []

    st.session_state.history.append(summary)

    st.write("📊 Simulation Summary")
    st.json(summary)

    # ✅ Build payload
    simulator_payload = {
        "location": st.session_state.get("location", "Custom"),
        "sunlight_hours": sunlight_hours,
        "num_nodes": len(nodes),
        "nodes": nodes,
        "summary": summary,
        "timestamp": datetime.now().isoformat()
    }

    simulator_url = generate_simulator_url(simulator_payload)

    if st.button("🚀 Send to Simulator", key="send_to_simulator"):
        st.markdown(f"[Click here to open Simulator with data]({simulator_url})", unsafe_allow_html=True)

else:
    st.warning("⚠️ No simulation results found. Please run the simulation first.")


if nodes and sunlight_hours:
    
    # ✅ Create the summary first
    summary = "This is a summary of the simulation results."

    # ✅ Payload and button go inside this block
    simulator_payload = {
        "location": st.session_state.get("location", "Custom"),
        "sunlight_hours": sunlight_hours,
        "num_nodes": num_nodes,
        "nodes": nodes,
        "summary": summary,
        "timestamp": datetime.now().isoformat()
    }

    simulator_url = generate_simulator_url(simulator_payload)

else:
    st.warning("⚠️ No simulation results found. Please run the simulation first.")
    simulator_url = None

# ✅ Button outside the block
if st.button("🚀 Send to Simulator", key="send_to_simulator") and simulator_url:
    st.markdown(f"[Open Simulator]({simulator_url})", unsafe_allow_html=True)

# 📄 Page Rendering Function

def render_page(page, results, history, labels, layout):
    if page == labels["visualize_results"]:
        st.header("📊 Simulation Narrative")

        if not results or not history:
            st.warning("No simulation data available. Please run the simulation first.")
            return

        st.subheader("🔋 Energy Distribution")
        for node, data in results.items():
            node_label = labels.get(node, node)
            st.write(f"• {node_label} generated **{data['energy']} kWh**")

        st.subheader("📈 Run History")
        for run in history:
            st.write(
                f"Run {run['Run']}: "
                f"Generated **{run['Total Generated']} kWh**, "
                f"Demand **{run['Total Demand']} kWh**, "
                f"Surplus **{run['Average Surplus']} kWh**"
            )

    elif page == labels["download_pdf"]:
        st.header("📄 " + labels["download_pdf"])

        if "history" in st.session_state and st.session_state.history:
            st.markdown(labels["download_report"])
            st.markdown(create_pdf(st.session_state.history[-1], labels), unsafe_allow_html=True)

            st.subheader("📜 " + labels["history"])
            df_history = pd.DataFrame(st.session_state.history)
            st.dataframe(df_history)
        else:
            st.warning(labels["run_first"])

    elif page == labels["home"]:
        st.header("🏠 Welcome")
        st.write("This is the home page of your solar microgrid simulation app.")

    elif page == labels["run_test"]:
        st.header("⚙️ Run Simulation")
        st.write("Click the button to run the simulation.")

        # 📊 Energy Distribution Chart
        st.subheader("⚡ Energy Distribution")
        if st.button("Show Energy Chart"):
            try:
                node_names = list(results.keys())
                energy_values = [node_data.get("energy", 0) for node_data in results.values()]

                fig, ax = plt.subplots()
                ax.bar(node_names, energy_values, color='orange')
                ax.set_ylabel("Energy (kWh)")
                ax.set_title("Energy Distribution per Node")
                ax.set_xticklabels(node_names, rotation=45, ha='right')
                st.pyplot(fig)
            except Exception as e:
                st.warning(f"Could not render energy chart: {e}")

        # 📈 Surplus vs Demand Line Chart
        st.subheader("📈 Surplus vs Demand Over Time")
        try:
            df = pd.DataFrame(history)
            fig = px.line(df, x='Run', y=['Total Generated', 'Total Demand', 'Average Surplus'],
                          markers=True, title="Simulation History")
            st.plotly_chart(fig)
        except Exception as e:
            st.warning(f"Could not render history chart: {e}")

        # 🗺️ Node Layout Diagram
        st.subheader("🗺️ Node Layout")
        try:
            edges = layout.get("edges", [(1, 2), (2, 3), (3, 4)])  # fallback if no layout edges
            G = nx.Graph()
            G.add_edges_from(edges)
            pos = nx.spring_layout(G)
            fig, ax = plt.subplots()
            nx.draw(G, pos, with_labels=True, node_color='lightblue', ax=ax)
            st.pyplot(fig)
        except Exception as e:
            st.warning(f"Could not render node layout: {e}")

        # 🌍 Simulation Narrative
        st.markdown("### 🌍 Simulation Narrative")
        st.markdown("""
        The Solar Umbrella Microgrid Simulator models the evolution of a modular energy node.  
        Starting as a climate pod, each umbrella can grow into an EV charging station, a building energy backbone,  
        and eventually a peer in a distributed energy system.

        This simulation explores how surplus energy scales with the number of umbrellas,  
        and how that surplus can be used to charge EVs or support building energy needs.

        Each node is not just a consumer or producer — it's a participant in a resilient, decentralized energy future.
        """)

        # 📜 History Section
        st.subheader("📜 History")
        if history:
            for i, item in enumerate(history):
                st.markdown(f"""
                **Run {i+1}**  
                🕒 Time: {item['Run']}  
                ⚡ Total Generated: {item['Total Generated']}  
                🔌 Total Demand: {item['Total Demand']}  
                📊 Average Surplus: {item['Average Surplus']}
                """)
        else:
            st.info("No history available.")

        # 🏷️ Labels Section
        st.subheader("🏷️ Labels")
        if labels:
            st.write(", ".join(labels.values()))
        else:
            st.info("No labels provided.")

# 📊 Results or PDF Page
if page == labels["home"]:
    st.header("🏠 Welcome")
    st.write("This is the home page of your solar microgrid simulation app.")

else:
    results = st.session_state.get("results", {})
    history = st.session_state.get("history", [])
    render_page(page, results, history, labels, layout)
