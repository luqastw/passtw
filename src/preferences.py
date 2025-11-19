from dataclasses import dataclass

@dataclass
class Preferences:
    use_upper: bool = False
    use_lower: bool = False
    use_nums: bool = False
    use_sims: bool = False
    length: int = 16