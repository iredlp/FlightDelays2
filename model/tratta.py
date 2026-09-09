from dataclasses import dataclass

from model.airport import Airport


@dataclass
class Tratta:
    aereoportoP: Airport
    aereoportoA: Airport
    peso: int

