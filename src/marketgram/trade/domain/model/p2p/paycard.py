from dataclasses import dataclass


@dataclass(frozen=True)
class Paycard:
    first6: str
    last4: str
    synonym: str

    def __str__(self) -> str:
        return (
            f'{self.first6[:5]} '
            f'{self.first6[4:]}** '
            f'**** {self.last4}'
        )