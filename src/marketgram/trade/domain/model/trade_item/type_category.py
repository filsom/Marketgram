from dataclasses import dataclass

from marketgram.common.errors import DomainError


@dataclass
class TypeCategory:
    name: str
    type_category_id: int = None

    def __post_init__(self) -> None:
        if len(self.name) == 1:
            raise DomainError()
        
        self.name = self.name.lower()