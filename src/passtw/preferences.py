from dataclasses import dataclass

@dataclass
class Preferences:
    upper: bool = True
    lower: bool = True
    nums: bool = True
    sims: bool = True