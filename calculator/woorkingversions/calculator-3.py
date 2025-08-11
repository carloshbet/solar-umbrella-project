def calculate_energy_output(width, length, coverage_efficiency, panel_efficiency, solar_irradiance, system_losses):
    surface_area_m2 = width * length * coverage_efficiency
    daily_energy_output_kWh = surface_area_m2 * panel_efficiency * solar_irradiance * system_losses
    return round(daily_energy_output_kWh, 2)

# Default values
width = float(input("Enter umbrella width in meters (e.g., 4): "))
length = float(input("Enter umbrella length in meters (e.g., 4): "))
coverage_efficiency = float(input("Enter usable panel surface ratio (e.g., 0.85): "))
panel_efficiency = float(input("Enter panel efficiency (e.g., 0.20 for 20%): "))
solar_irradiance = float(input("Enter avg daily solar irradiance in kWh/m²/day (e.g., 5.0): "))
system_losses = float(input("Enter system efficiency after losses (e.g., 0.85): "))

# Calculation
energy_output = calculate_energy_output(width, length, coverage_efficiency, panel_efficiency, solar_irradiance, system_losses)

print(f"\n⚡ Estimated Daily Energy Output: {energy_output} kWh/day")
