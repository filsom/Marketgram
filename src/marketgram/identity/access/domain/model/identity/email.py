from dataclasses import dataclass


@dataclass
class Email:
    value: str

    def __post_init__(self):
        self.value = self.value.lower()