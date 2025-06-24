INSTALLATION_POWER = 2.5
PANEL_EFFICIENCY = 0.2


def calculate_energy(sunshine_hours: float) -> float:
    return round(INSTALLATION_POWER * sunshine_hours * PANEL_EFFICIENCY, 2)