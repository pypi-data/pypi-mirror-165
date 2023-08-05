from dataclasses import dataclass

@dataclass
class Bike:
    name: str
    mass: float
    crr: float = 0.003  # tyre rolling resistance coefficient
