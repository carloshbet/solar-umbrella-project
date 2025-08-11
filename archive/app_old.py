import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO  # ✅ Must be before buffer is used
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
import plotly.express as px
import numpy as np

text = st.text_input("Enter text for your PDF", "Hello, PDF!")

# ✅ This only runs when the user clicks the button
if st.button("Generate PDF"):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    c.drawString(100, 750, text)  # ✅ uses user input
    c.save()

    st.download_button(
        label="Download PDF",
        data=buffer.getvalue(),
        file_name="report.pdf",
        mime="application/pdf"
    )

# --- App Configuration ---
# Line 8
def generate_combined_pdf(filename, cities, title, df):
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4
    y = height - 50

    # Title
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, y, title)
    y -= 30

    # Selected Cities Section
    if cities:
        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, y, "Selected Cities:")
        y -= 20
        c.setFont("Helvetica", 12)
        for city in cities:
            c.drawString(70, y, f"• {city}")
            y -= 15
            if y < 50:
                c.showPage()
                y = height - 50
    else:
        c.setFont("Helvetica", 12)
        c.drawString(50, y, "No cities selected.")
        y -= 20

    # Solar Data Section
    y -= 30
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, "Solar Data:")
    y -= 20

    # Column headers
    x_positions = [50, 200]
    c.setFont("Helvetica-Bold", 12)
    c.drawString(x_positions[0], y, "City")
    c.drawString(x_positions[1], y, "Solar Value")
    y -= 20

    # Table rows
    c.setFont("Helvetica", 10)
    for index, row in df.iterrows():
        c.drawString(x_positions[0], y, str(row["City"]))
        c.drawString(x_positions[1], y, str(row["Solar Value"]))
        y -= 15
        if y < 50:
            c.showPage()
            y = height - 50

    c.save()
# --- Translations or Text Labels ---
t = {
    "location": "Select Location",
    "city": "Choose Cities"
}

# --- Global City Data ---
city_data = {
    "Barcelona": 5.5,
    "Madrid": 6.0,
    "Berlin": 4.0,
    "Paris": 4.2,
    "Rome": 5.2,
    "Valencia": 5.8,
    "Amsterdam": 3.2,
    "Málaga": 6.5,
    "Seville": 6.7
}

# --- UI Layout ---
with st.expander(t["location"], expanded=True):
    selected_cities = st.multiselect(t["city"], list(city_data.keys()), default=["Barcelona"])

df = pd.DataFrame(list(city_data.items()), columns=["City", "Solar Value"])

if st.button("Download Combined PDF"):
    buffer = BytesIO()
    generate_combined_pdf(buffer, selected_cities, "Solar Report", df)

    st.download_button(
        label="Download PDF",
        data=buffer.getvalue(),
        file_name="solar_report.pdf",
        mime="application/pdf"
    )

# --- PDF Generation ---
def generate_combined_pdf(filename, cities, title, df):
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import A4 

    c = canvas.Canvas(filename, pagesize=A4)  # ✅ This must be here

    width, height = A4
    y = height - 50 

    # Title
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, y, title)
    y -= 30

    # Selected Cities Section
    if cities:
        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, y, "Selected Cities:")
        y -= 20
        c.setFont("Helvetica", 12)
        for city in cities:
            c.drawString(70, y, f"• {city}")
            y -= 15

# Add DataFrame content
    y -= 30
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, "Solar Data:")
    y -= 20
    c.setFont("Helvetica", 10)

# ✅ Define column positions
x_positions = [50, 150, 250]  # Adjust based on number of columns

# ✅ Loop through your row data
for index, row in df.iterrows():
    for i, col in enumerate(row):
        c.drawString(x_positions[i], y, str(col))
    y -= 20

    # Column headers
# Column headers
y -= 30
c.setFont("Helvetica-Bold", 12)

# Set starting position and column width
x_start = 50
col_width = 100

# ✅ Add this check
if df is None or df.empty:
    print("⚠️ DataFrame is empty or not defined.")
    x_positions = []  # Prevents crashing later
else:
    x_positions = [x_start + i * col_width for i in range(len(df.columns))]

# Column headers
y -= 30
c.setFont("Helvetica-Bold", 12)

for i, col in enumerate(df.columns):
    if i < len(x_positions):  # ✅ Prevent IndexError
        c.drawString(x_positions[i], y, col)

# 🔍 Debug print
print("Number of columns:", len(df.columns))
print("x_positions:", x_positions)
print("Columns:", df.columns.tolist())

for i, col in enumerate(df.columns):
    c.drawString(x_positions[i], y, col)

for i, col in enumerate(df.columns):
    c.drawString(x_positions[i], y, col)

    # Data rows
    y -= 20
    c.setFont("Helvetica", 10)
    for _, row in df.iterrows():
        for i, col in enumerate(df.columns):
            c.drawString(x_positions[i], y, str(row[col]))
        y -= 15
        if y < 50:
            c.showPage()
            y = height - 50

            
            if y < 50:
                c.showPage()
                y = height - 50
    else:
        c.setFont("Helvetica", 12)
        c.drawString(50, y, "No cities selected.")
        y -= 20
    
    # Continue with DataFrame content...

    # DataFrame
    y -= 30
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, "Solar Data:")
    y -= 20
    c.setFont("Helvetica", 10)
    for _, row in df.iterrows():
        line = ", ".join([f"{col}: {row[col]}" for col in df.columns])
        c.drawString(50, y, line)
        y -= 15
        if y < 50:
            c.showPage()
            y = height - 50

    c.save()
# --- Translations ---
translations = {
    "English": {
        "title": "Solar Umbrella Energy Dashboard",
        "location": "Location Settings",
        "city": "Select Your City",
        "umbrella_setup": "Umbrella Setup",
        "number": "Number of Solar Umbrellas",
        "size": "Select Umbrella Size",
        "custom_size": "Custom Size",
        "width": "Enter Width (m)",
        "height": "Enter Height (m)",
        "solar_params": "Solar Parameters",
        "efficiency": "Panel Efficiency (%)",
        "sunlight": "Average Sunlight Hours per Day",
        "cost": "Electricity Cost (€/kWh)",
        "battery": "Battery Storage",
        "capacity": "Battery Capacity (kWh)",
        "co2": "Environmental Impact",
        "results": "Results",
        "daily_energy": "Daily Energy Output (kWh)",
        "annual_energy": "Annual Energy Output (kWh)",
        "savings": "Annual Savings (€)",
        "co2_saved": "CO₂ Saved (kg/year)",
        "backup_days": "Battery provides approx.",
        "monthly_chart": "Monthly Energy Distribution",
        "download": "Download Your Report",
        "footer": "Made with ❤️ by Carlos H Betancourth"
    },
    # Add Spanish and Dutch translations as needed

    "Spanish": {
    "title": "Panel Solar Parasol - Panel de Control",
    "location": "Configuración de Ubicación",
    "city": "Selecciona tu Ciudad",
    "umbrella_setup": "Configuración del Parasol",
    "number": "Número de Parasoles Solares",
    "size": "Selecciona el Tamaño del Parasol",
    "custom_size": "Tamaño Personalizado",
    "width": "Introduce el Ancho (m)",
    "height": "Introduce la Altura (m)",
    "solar_params": "Parámetros Solares",
    "efficiency": "Eficiencia del Panel (%)",
    "sunlight": "Horas de Sol Promedio por Día",
    "cost": "Costo de Electricidad (€/kWh)",
    "battery": "Almacenamiento de Batería",
    "capacity": "Capacidad de la Batería (kWh)",
    "co2": "Impacto Ambiental",
    "results": "Resultados",
    "daily_energy": "Producción Diaria de Energía (kWh)",
    "annual_energy": "Producción Anual de Energía (kWh)",
    "savings": "Ahorro Anual (€)",
    "co2_saved": "CO₂ Ahorrado (kg/año)",
    "backup_days": "La batería proporciona aproximadamente",
    "monthly_chart": "Distribución Mensual de Energía",
    "download": "Descarga tu Informe",
    "footer": "Hecho con ❤️ por Carlos en Vidreres"
},
"Dutch": {
    "title": "Zonneparasol Energie Dashboard",
    "location": "Locatie-instellingen",
    "city": "Selecteer je Stad",
    "umbrella_setup": "Parasolconfiguratie",
    "number": "Aantal Zonneparasols",
    "size": "Selecteer Parasolgrootte",
    "custom_size": "Aangepaste Grootte",
    "width": "Voer Breedte in (m)",
    "height": "Voer Hoogte in (m)",
    "solar_params": "Zonneparameters",
    "efficiency": "Paneelefficiëntie (%)",
    "sunlight": "Gemiddeld Zonlicht per Dag",
    "cost": "Elektriciteitskosten (€/kWh)",
    "battery": "Batterijopslag",
    "capacity": "Batterijcapaciteit (kWh)",
    "co2": "Milieu-impact",
    "results": "Resultaten",
    "daily_energy": "Dagelijkse Energieopbrengst (kWh)",
    "annual_energy": "Jaarlijkse Energieopbrengst (kWh)",
    "savings": "Jaarlijkse Besparing (€)",
    "co2_saved": "CO₂ Bespaard (kg/jaar)",
    "backup_days": "Batterij levert ongeveer",
    "monthly_chart": "Maandelijkse Energieverdeling",
    "download": "Download je Rapport",
    "footer": "Gemaakt met ❤️ door Carlos in Vidreres"
},
"Catalan": {
    "title": "Parasol Solar - Tauler d'Energia",
    "location": "Configuració de la Ubicació",
    "city": "Selecciona la teva Ciutat",
    "umbrella_setup": "Configuració del Parasol",
    "number": "Nombre de Parasols Solars",
    "size": "Selecciona la Mida del Parasol",
    "custom_size": "Mida Personalitzada",
    "width": "Introdueix l'Ample (m)",
    "height": "Introdueix l'Alçada (m)",
    "solar_params": "Paràmetres Solars",
    "efficiency": "Eficiència del Panell (%)",
    "sunlight": "Hores Mitjanes de Sol al Dia",
    "cost": "Cost de l'Electricitat (€/kWh)",
    "battery": "Emmagatzematge de Bateria",
    "capacity": "Capacitat de la Bateria (kWh)",
    "co2": "Impacte Ambiental",
    "results": "Resultats",
    "daily_energy": "Producció Diària d'Energia (kWh)",
    "annual_energy": "Producció Anual d'Energia (kWh)",
    "savings": "Estalvi Anual (€)",
    "co2_saved": "CO₂ Estalviat (kg/any)",
    "backup_days": "La bateria proporciona aproximadament",
    "monthly_chart": "Distribució Mensual d'Energia",
    "download": "Descarrega el teu Informe",
    "footer": "Fet amb ❤️ per Carlos a Vidreres"
}
}
# --- Language Selection ---
language = st.selectbox("🌐 Choose Language", list(translations.keys()))
t = translations[language]
# --- Title ---
st.title("Solar Umbrella Energy Dashboard")
# Line 68 or earlier — insert this
import pandas as pd
monthly_energy_data = pd.DataFrame({
    "Month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
    "Energy (kWh)": [320, 280, 350, 400, 420, 450, 470, 460, 430, 390, 360, 340]
})
monthly_energy_data.set_index("Month", inplace=True)

# Line 69 — chart block starts


# Placeholder for image
show_image = False
if show_image:
    st.image("solar_diagram.png", caption="How Solar Umbrellas Work", use_container_width=True)
# Other dashboard elements...

# Placeholder for image
show_image = False
if show_image:
    st.image("solar_diagram.png", caption="How Solar Umbrellas Work", use_container_width=True)

# Continue with other widgets...

# --- Location Settings ---

# --- Global City Data ---
city_data = {
    "Barcelona": 5.5,
    "Madrid": 6.0,
    "Berlin": 4.0,
    "Paris": 4.2,
    "Rome": 5.2,
    "Valencia": 5.8,
    "Amsterdam": 3.2,
    "Málaga": 6.5,
    "Seville": 6.7
}

# --- Create DataFrame from city_data ---
df = pd.DataFrame(list(city_data.items()), columns=["City", "Solar Value"])

# --- UI Layout ---
with st.expander(t["location"], expanded=True):
    selected_cities = st.multiselect(t["city"], list(city_data.keys()), default=["Barcelona"])

st.write("Available cities:", city_data.keys())  # 👈 Debug line
# --- Umbrella Setup ---
with st.expander(t["umbrella_setup"], expanded=True):
    num_umbrellas = st.slider(t["number"], min_value=1, max_value=20, value=1)
    umbrella_sizes = {
        "4 x 4 m": 16.0,
        "4.5 x 4.5 m": 20.25,
        "5 x 5 m": 25.0,
        t["custom_size"]: None
    }
    selected_size = st.selectbox(t["size"], list(umbrella_sizes.keys()))

    if selected_size == t["custom_size"]:
        width = st.number_input(t["width"], min_value=1.0, step=0.1)
        height = st.number_input(t["height"], min_value=1.0, step=0.1)
        panel_area = width * height
    else:
        panel_area = umbrella_sizes[selected_size]

    total_panel_area = panel_area * num_umbrellas

# --- Solar Parameters ---
with st.expander(t["solar_params"], expanded=True):
    efficiency = st.slider(t["efficiency"], min_value=10, max_value=25, value=18)
    cost_per_kwh = st.number_input(t["cost"], min_value=0.01, value=0.20)

# --- Battery Storage ---
with st.expander(t["battery"], expanded=True):
    battery_capacity_kwh = st.number_input(t["capacity"], min_value=0.0, value=10.0)

# --- Environmental Impact ---
co2_per_kwh = 0.25

# --- Results ---
st.header(t["results"])
results = []

for city in selected_cities:
    sunlight_hours = city_data[city]
    daily_energy = total_panel_area * (efficiency / 100) * sunlight_hours
    annual_energy = daily_energy * 365
    savings = annual_energy * cost_per_kwh
    backup_days = battery_capacity_kwh / daily_energy if daily_energy else 0
    co2_saved = annual_energy * co2_per_kwh

    results.append({
        "City": city,
        t["daily_energy"]: f"{daily_energy:.2f}",
        t["annual_energy"]: f"{annual_energy:.0f}",
        t["savings"]: f"{savings:.2f}",
        t["co2_saved"]: f"{co2_saved:.0f}",
        t["backup_days"]: f"{backup_days:.1f} days"
    })

df_results = pd.DataFrame(results)
st.dataframe(df_results, use_container_width=True)

# --- Line Chart Narrative ---
# --- Tabs for Chart Navigation ---
tab1, tab2 = st.tabs(["📈 Monthly Trend", "⚡ Production Overview"])

# --- Tab 1: Monthly Energy Trend by City ---
with tab1:
    st.markdown("""
    📈 **Monthly Energy Trend by City**  
    This line chart shows how much solar energy is generated each month for each selected city.  
    It helps visualize seasonal patterns and compare energy output across locations.
    """)
    fig_line, ax_line = plt.subplots()
    for city in selected_cities:
        sunlight_hours = city_data[city]
        daily_energy = total_panel_area * (efficiency / 100) * sunlight_hours
        monthly_energy = [daily_energy * days for days in [31,28,31,30,31,30,31,31,30,31,30,31]]
        ax_line.plot(range(1, 13), monthly_energy, label=city)

    ax_line.set_xlabel("Month")
    ax_line.set_ylabel("Energy (kWh)")
    ax_line.set_title("Monthly Energy Output by City")
    ax_line.legend()
    st.pyplot(fig_line)

# --- Tab 2: Energy Production Overview ---
with tab2:
    st.markdown("""
    ⚡ **Energy Production Overview**  
    This bar chart shows the total annual energy output for each selected city, based on your umbrella setup.  
    It provides a quick comparison of overall performance across locations.
    """)

    production_data = {}
    for city in selected_cities:
        sunlight_hours = city_data[city]
        daily_energy = total_panel_area * (efficiency / 100) * sunlight_hours
        annual_energy = daily_energy * 365
        production_data[city] = annual_energy

    # Convert to DataFrame and plot
    energy_df = pd.DataFrame({
        "City": list(production_data.keys()),
        "Annual Energy (kWh)": list(production_data.values())
    })
# Sort cities by energy output
energy_df = energy_df.sort_values(by="Annual Energy (kWh)", ascending=False)

fig = px.bar(
    energy_df,
    x="City",
    y="Annual Energy (kWh)",
    title="⚡ Energy Production Overview",
    labels={"Annual Energy (kWh)": "Annual Energy (kWh)", "City": "City"},
    color="City"
)
st.plotly_chart(fig)

# --- Stacked Bar Chart Narrative ---
st.markdown("""
📊 **Stacked Monthly Energy by City**  
This stacked bar chart displays the combined monthly energy output from all selected cities.  
It highlights how each city contributes to the total energy production over the year.
""")
# --- PDF Export ---
st.subheader(t["download"])

if st.button("📄 Create PDF"):
    generate_combined_pdf("solar_report.pdf", selected_cities, t["title"], df_results)

    with open("solar_report.pdf", "rb") as f:
        st.download_button(
            label="📄 Download PDF",
            data=f,
            file_name="solar_report.pdf",
            mime="application/pdf"
        )

# --- Footer ---
st.caption(t["footer"])





























































