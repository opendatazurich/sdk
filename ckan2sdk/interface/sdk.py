from dataclasses import dataclass, field, asdict
from typing import List


@dataclass
class SDK:
    """This dataclass defines what the SDK expects as input for the import use case"""

    label: str
    # tags: List[str] = field(default_factory=list)

    def to_json(self):
        return asdict(self)

    def __post_init__(self):
        self.label = self.label.strip()
