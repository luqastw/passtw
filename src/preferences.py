from dataclasses import dataclass

@dataclass
class Preferences:
    upper: bool = True
    lower: bool = False
    nums: bool = False
    sims: bool = False