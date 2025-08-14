# Parameters
import math

# Umbrella size options (in meters)
width = 4    # could be 4 or 5 for 4x4 or 5x5
length = 4

# Panel coverage factor (to account for gaps, folds, joints)
coverage_efficiency = 0.85  # 85% of surface is covered by PV panels

# Usable surface area
surface_area_m2 = width * length * coverage_efficiency  # in m²

# Panel efficiency (depends on PV technology, e.g., 18–22%)
panel_efficiency = 0.20  # 20%

# Average solar irradiance (kWh/m²/day)
solar_irradiance = 5.0  # You can adjust depending on the city

# System losses (inverter, temperature, wiring) ~15%
system_losses = 0.85

# Daily energy output (in kWh/day)
daily_energy_output_kWh = surface_area_m2 * panel_efficiency * solar_irradiance * system_losses

# Print results
print(f"Estimated daily energy output for {width}x{length}m umbrella: {daily_energy_output_kWh:.2f} kWh/day")
