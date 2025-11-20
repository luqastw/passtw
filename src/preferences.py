from dataclasses import dataclass

@dataclass
class Preferences:
    upper: bool = False
    lower: bool = False
    nums: bool = False
    sims: bool = False