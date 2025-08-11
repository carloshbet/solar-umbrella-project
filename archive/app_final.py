import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

# --- Page Config ---
st.set_page_config(page_title="Solar Dashboard", layout="wide")

# --- City Data ---
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

# --- Translations ---
translations = {
    "English": {
        "Solar Radiation": "Solar Radiation",
        "City": "City",
        "Download PDF": "Download PDF",
        "Umbrella Tilt": "Umbrella Tilt Angle (°)",
        "Umbrella Size": "Umbrella Size (m)",
        "Number of Umbrellas": "Number of Umbrellas",
        "Monthly Energy": "Estimated Monthly Energy (kWh)",
        "Total Energy": "Total Energy Output (kWh)"
    },
    "Spanish": {
        "Solar Radiation": "Radiación Solar",
        "City": "Ciudad",
        "Download PDF": "Descargar PDF",
        "Umbrella Tilt": "Ángulo de Inclinación (°)",
        "Umbrella Size": "Tamaño del Paraguas (m)",
        "Number of Umbrellas": "Número de Paraguas",
        "Monthly Energy": "Energía Mensual Estimada (kWh)",
        "Total Energy": "Producción Total de Energía (kWh)"
    },
    "Dutch": {
        "Solar Radiation": "Zonnestraling",
        "City": "Stad",
        "Download PDF": "PDF Downloaden",
        "Umbrella Tilt": "Parasolhoek (°)",
        "Umbrella Size": "Parasolgrootte (m)",
        "Number of Umbrellas": "Aantal Parasols",
        "Monthly Energy": "Geschatte Maandelijkse Energie (kWh)",
        "Total Energy": "Totale Energieproductie (kWh)"
    },
    "Catalan": {
        "Solar Radiation": "Radiació Solar",
        "City": "Ciutat",
        "Download PDF": "Descarregar PDF",
        "Umbrella Tilt": "Inclinació del Para-sol (°)",
        "Umbrella Size": "Mida del Para-sol (m)",
        "Number of Umbrellas": "Nombre de Para-sols",
        "Monthly Energy": "Energia Mensual Estimada (kWh)",
        "Total Energy": "Producció Total d'Energia (kWh)"
    }
}

# --- Sidebar ---
st.sidebar.title("Settings")
language = st.sidebar.selectbox("Choose language", list(translations.keys()))
labels = translations[language]
title = st.sidebar.text_input("Report Title", "Solar Data Report")
selected_cities = st.sidebar.multiselect("Select Cities", list(city_data.keys()), default=["Barcelona"])
tilt_angle = st.sidebar.slider(labels["Umbrella Tilt"], 0, 90, 30)
umbrella_size = st.sidebar.selectbox(labels["Umbrella Size"], ["4.0 x 4.0", "4.5 x 4.5", "5.0 x 5.0"])
num_umbrellas = st.sidebar.number_input(labels["Number of Umbrellas"], min_value=1, max_value=100, value=1)

# --- Umbrella Area ---
size_map = {
    "4.0 x 4.0": 16.0,
    "4.5 x 4.5": 20.25,
    "5.0 x 5.0": 25.0
}
panel_area = size_map[umbrella_size]

# --- DataFrame ---
df = pd.DataFrame(list(city_data.items()), columns=["City", "Solar Value"])
filtered_df = df[df["City"].isin(selected_cities)]

# --- Energy Calculation ---
def calculate_energy(radiation, tilt, area, count):
    efficiency = max(0.5, np.cos(np.radians(tilt)))
    monthly = radiation * area * efficiency * 30
    return round(monthly * count, 2)

filtered_df["Total Energy"] = filtered_df["Solar Value"].apply(
    lambda r: calculate_energy(r, tilt_angle, panel_area, num_umbrellas)
)

# --- Metrics ---
avg_energy = round(filtered_df["Total Energy"].mean(), 2)
col1, col2 = st.columns(2)
col1.metric(label=labels["Total Energy"], value=f"{avg_energy} kWh")
col2.metric(label=labels["City"], value=f"{len(selected_cities)} selected")

# --- Charts ---
st.title(title)
tab1, tab2, tab3 = st.tabs([labels["Solar Radiation"], labels["Total Energy"], labels["City"]])

with tab1:
    fig1 = px.bar(filtered_df, x="City", y="Solar Value", color="City",
                  labels={"Solar Value": labels["Solar Radiation"], "City": labels["City"]})
    st.plotly_chart(fig1, use_container_width=True)

with tab2:
    fig2 = px.bar(filtered_df, x="City", y="Total Energy", color="City",
                  labels={"Total Energy": labels["Total Energy"], "City": labels["City"]})
    st.plotly_chart(fig2, use_container_width=True)

with tab3:
    st.dataframe(filtered_df)

# --- PDF Generation ---
def generate_combined_pdf(filename, cities, title, df, tilt, size_label, area, count):
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4
    y = height - 50

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, y, title)
    y -= 30

    c.setFont("Helvetica", 12)
    c.drawString(50, y, f"{labels['Umbrella Tilt']}: {tilt}°")
    y -= 20
    c.drawString(50, y, f"{labels['Umbrella Size']}: {size_label} ({area} m²)")
    y -= 20
    c.drawString(50, y, f"{labels['Number of Umbrellas']}: {count}")
    y -= 30

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

    y -= 30
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, "Solar Data:")
    y -= 20

    x_positions = [50, 200, 350]
    c.setFont("Helvetica-Bold", 12)
    c.drawString(x_positions[0], y, "City")
    c.drawString(x_positions[1], y, "Radiation")
    c.drawString(x_positions[2], y, "Total Energy")
    y -= 20

    c.setFont("Helvetica", 10)
    for _, row in df.iterrows():
        c.drawString(x_positions[0], y, str(row["City"]))
        c.drawString(x_positions[1], y, f"{row['Solar Value']} kWh/m²")
        c.drawString(x_positions[2], y, f"{row['Total Energy']} kWh")
        y -= 15
        if y < 50:
            c.showPage()
            y = height - 50

    c.save()

# --- PDF Export ---
buffer = BytesIO()
generate_combined_pdf(buffer, selected_cities, title, filtered_df, tilt_angle, umbrella_size, panel_area, num_umbrellas)
buffer.seek(0)

st.download_button(
    label=labels["Download PDF"],
    data=buffer,
    file_name="solar_dashboard_report.pdf",
    mime="application/pdf"
)
