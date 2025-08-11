# solar_evolution_simulator.py
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import networkx as nx
import json
from math import isfinite

# Hardcoded city electricity prices
CITIES = {
    "Madrid": 0.25,
    "Barcelona": 0.26,
    "Malaga": 0.24,
    "Sevilla": 0.23,
    "Amsterdam": 0.29,
    "Berlin": 0.30,
    "Paris": 0.28,
    "Burkina Faso": 0.22,
    "Nairobi": 0.21,
    "Tokyo": 0.32,
    "Los Angeles": 0.27
}

LANG = {
    "en": {
        "language_name": "English",
        "welcome_title": "🔆 Solar Energy Evolution Simulator",
        "narrative_intro": """\
Our mission is to address the challenges of high energy consumption, transition to renewables, electrification of mobility, and urban heat mitigation—all while providing shade to reduce heat waves and urban heat island effect.

This solar umbrella adds value to the traditional cultural umbrella as a protector against heat and rain, by becoming a digital-physical service platform that integrates renewable energy production, electric vehicle charging, and microgrid energy sales, and still creates shadows and coolness.

Welcome to the Solar Evolution Simulator. This simulator serves as the brain and control center of our solar umbrella and Terrazas ecosystem — linking energy production, mobility, finance, and urban resilience in one interactive tool. It models the evolution from a simple solar umbrella to a climate-resilient energy and mobility node. Use it to explore how adding umbrellas, batteries, and services changes energy output, CO₂ savings, and financial viability.

This tool helps you model solar energy output, storage, financial viability, and microgrid energy sharing. This simulator helps visualize and quantify how solar umbrellas evolve from simple shading devices to integral components of sustainable urban energy ecosystems. Select your city, define your stage of evolution, and customize parameters to explore energy production, carbon savings, battery backup, and peer-to-peer energy flows in microgrid ecosystems.

Choose a tab to start exploring.
""",
        "strategic_narrative": """\
By incorporating these services, the initially higher capital cost of advanced foldable umbrellas is offset by diversified revenue streams, accelerating loan repayment and increasing profitability.

This approach directly supports BBVA's goals of sustainability, urban resilience, and financial viability, turning infrastructure investments into climate-positive business models.
""",
        "select_language": "Select language",
        "select_city": "Select city",
        "select_stage": "Select evolution stage",
        "evolution_stages": ["Basic Umbrella", "Solar Terraza", "EV Oasis", "Building Backbone", "Peer Node"],
        "cities": list(CITIES.keys()),
        "simulator_parameters": "⚙️ Simulator parameters",
        "umbrella_width": "Umbrella width (m)",
        "umbrella_length": "Umbrella length (m)",
        "coverage_efficiency": "Panel coverage efficiency (fraction)",
        "panel_efficiency": "Panel efficiency (fraction)",
        "system_losses": "System efficiency after losses (fraction)",
        "electricity_price": "Electricity price (€/kWh)",
        "battery_header": "🔋 Battery storage",
        "battery_capacity": "Battery capacity (kWh)",
        "battery_efficiency": "Battery efficiency (fraction)",
        "days_autonomy": "Required days of autonomy",
        "financial_header": "💰 Financial / loan",
        "loan_amount": "Loan amount (€)",
        "interest_rate": "Annual interest rate (%)",
        "loan_term": "Loan term (years)",
        "revenue_header": "Additional revenue streams",
        "rev_ev_charging": "EV charging revenue (€/year)",
        "rev_energy_sales": "Energy sales revenue (€/year)",
        "tabs": ["Basic Calculator", "Energy Microgrid", "How to use"],
        "download_json": "📥 Download configuration (JSON)",
        "download_csv": "📥 Download configuration (CSV)",
        "scenario_comparison": "📊 Scenario comparison",
        "microgrid_title": "🌐 Energy microgrid visualization",
        "node_surplus": "Surplus (kWh)",
        "node_deficit": "Deficit (kWh)",
        "units_needed_text": "Units needed to meet target (approx):",
        "target_energy": "Target daily energy (kWh)",
        "basic_calc_desc": "Adjust parameters and compare scenarios below.",
        "scenario_1": "Scenario 1",
        "scenario_2": "Scenario 2",
        "compare_btn": "Compare scenarios",
    },
    "es": {
        "language_name": "Español",
        "welcome_title": "🔆 Simulador de Evolución de Energía Solar",
        "narrative_intro": """\
Nuestra misión es abordar los desafíos del alto consumo energético, la transición a energías renovables, la electrificación de la movilidad y la mitigación del calor urbano — todo mientras proporcionamos sombra para reducir las olas de calor y el efecto isla de calor urbano.

Esta sombrilla solar añade valor a la sombrilla cultural tradicional como protectora contra el calor y la lluvia, al convertirse en una plataforma de servicios físico-digital que integra la producción de energía renovable, carga de vehículos eléctricos y venta de energía en microredes, y aún crea sombra y frescor.

Bienvenido al Simulador de Evolución Solar. Este simulador es el cerebro y centro de control de nuestro ecosistema de sombrillas solares y terrazas — vinculando producción de energía, movilidad, finanzas y resiliencia urbana en una herramienta interactiva. Modela la evolución desde una simple sombrilla solar hasta un nodo climático y de movilidad resiliente. Úsalo para explorar cómo la adición de sombrillas, baterías y servicios cambia la producción de energía, ahorro de CO₂ y viabilidad financiera.

Esta herramienta te ayuda a modelar la producción de energía solar, almacenamiento, viabilidad financiera y compartición energética en microredes. Este simulador visualiza y cuantifica cómo las sombrillas solares evolucionan de simples dispositivos de sombra a componentes integrales de ecosistemas urbanos sostenibles. Selecciona tu ciudad, define la etapa de evolución y personaliza parámetros para explorar producción energética, ahorro de carbono, respaldo con baterías y flujos entre pares en microredes.

Elige una pestaña para comenzar a explorar.
""",
        "strategic_narrative": """\
Al incorporar estos servicios, el mayor coste de capital inicial de las sombrillas plegables avanzadas se compensa con fuentes diversificadas de ingresos, acelerando la amortización del préstamo y aumentando la rentabilidad.

Este enfoque apoya directamente los objetivos de BBVA en sostenibilidad, resiliencia urbana y viabilidad financiera, transformando inversiones en infraestructura en modelos de negocio positivos para el clima.
""",
        "select_language": "Seleccionar idioma",
        "select_city": "Seleccionar ciudad",
        "select_stage": "Seleccionar etapa",
        "evolution_stages": ["Sombrilla Básica", "Terraza Solar", "Oasis EV", "Columna Energética", "Nodo Par"],
        "cities": list(CITIES.keys()),
        "simulator_parameters": "⚙️ Parámetros del simulador",
        "umbrella_width": "Ancho sombrilla (m)",
        "umbrella_length": "Largo sombrilla (m)",
        "coverage_efficiency": "Eficiencia de cobertura (fracción)",
        "panel_efficiency": "Eficiencia del panel (fracción)",
        "system_losses": "Eficiencia del sistema tras pérdidas (fracción)",
        "electricity_price": "Precio electricidad (€/kWh)",
        "battery_header": "🔋 Batería",
        "battery_capacity": "Capacidad de batería (kWh)",
        "battery_efficiency": "Eficiencia batería (fracción)",
        "days_autonomy": "Días de autonomía requeridos",
        "financial_header": "💰 Financiero / préstamo",
        "loan_amount": "Monto préstamo (€)",
        "interest_rate": "Tasa de interés anual (%)",
        "loan_term": "Plazo (años)",
        "revenue_header": "Fuentes de ingreso adicionales",
        "rev_ev_charging": "Ingresos carga EV (€/año)",
        "rev_energy_sales": "Ingresos venta energía (€/año)",
        "tabs": ["Calculadora básica", "Microred energética", "Cómo usar"],
        "download_json": "📥 Descargar configuración (JSON)",
        "download_csv": "📥 Descargar configuración (CSV)",
        "scenario_comparison": "📊 Comparación de escenarios",
        "microgrid_title": "🌐 Visualización de microred",
        "node_surplus": "Excedente (kWh)",
        "node_deficit": "Déficit (kWh)",
        "units_needed_text": "Unidades necesarias para objetivo (aprox):",
        "target_energy": "Energía diaria objetivo (kWh)",
        "basic_calc_desc": "Ajusta parámetros y compara escenarios abajo.",
        "scenario_1": "Escenario 1",
        "scenario_2": "Escenario 2",
        "compare_btn": "Comparar escenarios",
    },
    "nl": {
        "language_name": "Nederlands",
        "welcome_title": "🔆 Zonne-Energie Evolutie Simulator",
        "narrative_intro": "Onze missie is ... (tekst in het Nederlands).",
        "strategic_narrative": "Door deze diensten ... (tekst NL).",
        "select_language": "Selecteer taal",
        "select_city": "Selecteer stad",
        "select_stage": "Selecteer stadium",
        "evolution_stages": ["Basis Parasol", "Zonne Terraza", "EV Oase", "Energie Ruggegraat", "Peer Node"],
        "cities": list(CITIES.keys()),
        "simulator_parameters": "⚙️ Simulator parameters",
        "umbrella_width": "Parasol breedte (m)",
        "umbrella_length": "Parasol lengte (m)",
        "coverage_efficiency": "Dek-efficiëntie (fract)",
        "panel_efficiency": "Paneel efficiëntie (fract)",
        "system_losses": "Systeem efficiëntie na verliezen (fract)",
        "electricity_price": "Elektriciteitsprijs (€/kWh)",
        "battery_header": "🔋 Batterij",
        "battery_capacity": "Batterij capaciteit (kWh)",
        "battery_efficiency": "Batterij efficiëntie (fract)",
        "days_autonomy": "Benodigde autonomie (dagen)",
        "financial_header": "💰 Financiën / lening",
        "loan_amount": "Lening bedrag (€)",
        "interest_rate": "Jaarlijkse rente (%)",
        "loan_term": "Looptijd (jaren)",
        "revenue_header": "Aanvullende inkomsten",
        "rev_ev_charging": "EV-laadinkomsten (€/jr)",
        "rev_energy_sales": "Energie-verkoopinkomsten (€/jr)",
        "tabs": ["Basis calculator", "Microgrid", "Handleiding"],
        "download_json": "📥 Configuratie (JSON)",
        "download_csv": "📥 Configuratie (CSV)",
        "scenario_comparison": "📊 Scenario vergelijking",
        "microgrid_title": "🌐 Microgrid visualisatie",
        "node_surplus": "Overschot (kWh)",
        "node_deficit": "Tekort (kWh)",
        "units_needed_text": "Benodigde units (ongeveer):",
        "target_energy": "Doel kWh/dag",
        "basic_calc_desc": "Pas parameters aan en vergelijk scenario's hieronder.",
        "scenario_1": "Scenario 1",
        "scenario_2": "Scenario 2",
        "compare_btn": "Vergelijk scenario's",
    }
}

def calculate_energy_output(width, length, coverage_eff, panel_eff, irradiance_kwh=5.0, system_losses=1.0):
    surface_area = width * length
    effective_area = surface_area * coverage_eff
    daily_kwh = effective_area * panel_eff * irradiance_kwh * system_losses
    return round(daily_kwh, 3)

def calculate_co2_savings(kwh, co2_factor=0.3):
    return round(kwh * co2_factor, 2)

def calculate_cost_savings(kwh, price_per_kwh):
    return round(kwh * price_per_kwh, 2)

def calculate_battery_backup(daily_output, battery_capacity, efficiency, days_autonomy):
    usable = battery_capacity * efficiency
    backup_days = round(usable / daily_output, 2) if daily_output > 0 else 0
    meets = backup_days >= days_autonomy
    return usable, backup_days, meets

def loan_annuity_payment(principal, annual_rate_pct, years):
    r = annual_rate_pct / 100.0
    n = years
    if r == 0:
        return principal / n
    annuity = principal * (r * (1 + r) ** n) / ((1 + r) ** n - 1)
    return annuity

def simulate_energy_exchange(nodes):
    for node in nodes:
        node['net'] = round(node.get('generation_kwh', 0) - node.get('demand_kwh', 0), 3)

    surplus_nodes = [n for n in nodes if n['net'] > 0]
    deficit_nodes = [n for n in nodes if n['net'] < 0]

    total_surplus = sum(n['net'] for n in surplus_nodes)
    total_deficit = sum(-n['net'] for n in deficit_nodes)

    flows = {}
    if total_surplus <= 0 or total_deficit <= 0:
        for n in nodes:
            n['surplus_kwh'] = max(n['net'], 0)
            n['deficit_kwh'] = max(-n['net'], 0)
        return nodes, flows

    for s in surplus_nodes:
        s_available = s['net']
        for d in deficit_nodes:
            share = (-d['net']) / total_deficit if total_deficit else 0
            transfer = round(min(s_available, share * total_surplus), 3)
            if transfer <= 0:
                continue
            s_available -= transfer
            d['net'] += transfer
            flows[(s['name'], d['name'])] = flows.get((s['name'], d['name']), 0) + transfer

    for n in nodes:
        n['surplus_kwh'] = round(max(n['net'], 0), 3)
        n['deficit_kwh'] = round(max(-n['net'], 0), 3)

    return nodes, flows

def main():
    st.set_page_config(page_title="Solar Evolution Simulator", layout="wide")

    # Sidebar
    st.sidebar.title("Solar Umbrella Simulator")

    lang_choice = st.sidebar.selectbox(
        "🌐 " + "Select language",
        options=["en", "es", "nl"],
        format_func=lambda x: LANG[x]["language_name"],
        index=0,
    )
    L = LANG[lang_choice]

    # Sidebar narratives - only short strategic narrative here
    st.sidebar.markdown(f"### {L['welcome_title']}")
    st.sidebar.markdown(L["strategic_narrative"])
    st.sidebar.markdown("---")

    city = st.sidebar.selectbox(L["select_city"], options=L["cities"])
    stage = st.sidebar.selectbox(L["select_stage"], options=L["evolution_stages"])
    st.sidebar.markdown("---")

    st.sidebar.markdown(L["simulator_parameters"])
    width = st.sidebar.slider(L["umbrella_width"], 1.0, 10.0, 4.0, 0.1)
    length = st.sidebar.slider(L["umbrella_length"], 1.0, 10.0, 4.0, 0.1)
    coverage_eff = st.sidebar.slider(L["coverage_efficiency"], 0.0, 1.0, 0.75, 0.01)
    panel_eff = st.sidebar.slider(L["panel_efficiency"], 0.0, 1.0, 0.18, 0.01)
    system_losses = st.sidebar.slider(L["system_losses"], 0.0, 1.0, 0.85, 0.01)
    st.sidebar.markdown("---")

    price_per_kwh = CITIES.get(city, 0.25)

    st.sidebar.header(L["battery_header"])
    battery_capacity = st.sidebar.number_input(L["battery_capacity"], min_value=0.0, value=10.0, step=1.0)
    battery_efficiency = st.sidebar.slider(L["battery_efficiency"], 0.0, 1.0, 0.9, 0.01)
    days_autonomy = st.sidebar.number_input(L["days_autonomy"], min_value=0, value=2, step=1)
    st.sidebar.markdown("---")

    st.sidebar.header(L["financial_header"])
    loan_amount = st.sidebar.number_input(L["loan_amount"], min_value=0.0, value=7000.0, step=100.0)
    interest_rate = st.sidebar.slider(L["interest_rate"], 0.0, 20.0, 5.0, 0.1)
    loan_term = st.sidebar.number_input(L["loan_term"], 1, 30, 10, 1)
    st.sidebar.markdown("---")

    st.sidebar.header(L["revenue_header"])
    rev_ev_charging = st.sidebar.number_input(L["rev_ev_charging"], min_value=0.0, value=1000.0, step=100.0)
    rev_energy_sales = st.sidebar.number_input(L["rev_energy_sales"], min_value=0.0, value=2000.0, step=100.0)

    # Main page content
    st.title(L["welcome_title"])
    st.markdown(L["narrative_intro"])

    # Compute basic energy output
    daily_per_umbrella = calculate_energy_output(width, length, coverage_eff, panel_eff, 5.0, system_losses)
    annual_energy = daily_per_umbrella * 365

    st.subheader("Energy Output & Savings")
    st.write(f"- Daily energy production per umbrella: **{daily_per_umbrella} kWh**")
    co2_savings = calculate_co2_savings(annual_energy)
    st.write(f"- Annual CO₂ savings: **{co2_savings} kg CO₂**")
    cost_savings = calculate_cost_savings(annual_energy, price_per_kwh)
    st.write(f"- Annual energy cost savings: **€{cost_savings}**")

    # Battery backup
    usable_battery, backup_days, meets_autonomy = calculate_battery_backup(daily_per_umbrella, battery_capacity, battery_efficiency, days_autonomy)
    st.subheader("Battery Backup")
    st.write(f"- Usable battery capacity: **{usable_battery:.2f} kWh**")
    st.write(f"- Days of backup (autonomy): **{backup_days} days**")
    st.write(f"- Meets autonomy requirement of {days_autonomy} days: **{'Yes' if meets_autonomy else 'No'}**")

    # Financial calculations
    annuity = loan_annuity_payment(loan_amount, interest_rate, loan_term)
    annual_revenue = cost_savings + rev_ev_charging + rev_energy_sales
    annual_expenses = annuity * 12
    annual_net_cash_flow = annual_revenue - annual_expenses

    if annual_net_cash_flow > 0:
        payback_years = loan_amount / annual_net_cash_flow
    else:
        payback_years = float('inf')

    payback_str = f"{payback_years:.1f}" if isfinite(payback_years) else "∞"

    st.subheader("Financials")
    st.write(f"- Annual revenue streams: **€{annual_revenue:.2f}**")
    st.write(f"- Annual loan payment: **€{annual_expenses:.2f}**")
    st.write(f"- Approximate payback (years): **{payback_str}**")

    # Tabs
    tabs = st.tabs(L["tabs"])

    # Basic Calculator Tab with Scenario Comparison
    with tabs[0]:
        st.subheader(L["tabs"][0])
        st.markdown(L["basic_calc_desc"])

        # Scenario 1 inputs
        st.markdown(f"### {L['scenario_1']}")
        w1 = st.slider("Width (m)", 1.0, 10.0, 4.0, 0.1, key="w1")
        l1 = st.slider("Length (m)", 1.0, 10.0, 4.0, 0.1, key="l1")
        cov1 = st.slider("Coverage efficiency", 0.0, 1.0, 0.75, 0.01, key="cov1")
        pan1 = st.slider("Panel efficiency", 0.0, 1.0, 0.18, 0.01, key="pan1")

        energy1 = calculate_energy_output(w1, l1, cov1, pan1, 5.0, system_losses)

        # Scenario 2 inputs
        st.markdown(f"### {L['scenario_2']}")
        w2 = st.slider("Width (m)", 1.0, 10.0, 3.0, 0.1, key="w2")
        l2 = st.slider("Length (m)", 1.0, 10.0, 3.0, 0.1, key="l2")
        cov2 = st.slider("Coverage efficiency", 0.0, 1.0, 0.60, 0.01, key="cov2")
        pan2 = st.slider("Panel efficiency", 0.0, 1.0, 0.15, 0.01, key="pan2")

        energy2 = calculate_energy_output(w2, l2, cov2, pan2, 5.0, system_losses)

        if st.button(L["compare_btn"]):
            st.write(f"Scenario 1 energy output: **{energy1} kWh/day**")
            st.write(f"Scenario 2 energy output: **{energy2} kWh/day**")

            diff = energy1 - energy2
            st.write(f"Difference: **{diff:.2f} kWh/day**")

    # Microgrid visualization tab
    with tabs[1]:
        st.subheader(L["microgrid_title"])

        nodes = [
            {"name": "Umbrella 1", "generation_kwh": daily_per_umbrella, "demand_kwh": daily_per_umbrella * 0.8},
            {"name": "Umbrella 2", "generation_kwh": daily_per_umbrella * 0.9, "demand_kwh": daily_per_umbrella},
            {"name": "Umbrella 3", "generation_kwh": daily_per_umbrella * 1.1, "demand_kwh": daily_per_umbrella * 1.0},
        ]
        updated_nodes, flows = simulate_energy_exchange(nodes)

        st.write("### Nodes energy surplus and deficits (kWh):")
        for n in updated_nodes:
            st.write(f"- {n['name']}: Surplus {n['surplus_kwh']} kWh, Deficit {n['deficit_kwh']} kWh")

        st.write("### Energy flows between nodes (kWh):")
        if flows:
            for (src, dst), amount in flows.items():
                st.write(f"- {src} → {dst}: {amount} kWh")
        else:
            st.write("- No energy flows")

    # How to use tab
    with tabs[2]:
        st.subheader(L["tabs"][2])
        st.markdown("""
Use this simulator to model the energy, financial, and environmental impacts of deploying solar umbrellas at different stages of evolution. Adjust parameters in the sidebar and tabs to see real-time impacts and compare scenarios.

You can explore:
- How size and efficiency impact energy output.
- Battery backup capabilities.
- Financial viability and payback periods.
- Energy sharing between umbrellas in a microgrid.

Start by selecting your city and evolution stage in the sidebar.
""")

if __name__ == "__main__":
    main()








