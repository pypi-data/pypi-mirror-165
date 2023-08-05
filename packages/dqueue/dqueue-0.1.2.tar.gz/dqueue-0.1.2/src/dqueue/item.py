# -*- coding: utf-8 -*-
import uuid
from dataclasses import dataclass, field


@dataclass
class Item:
    data: str
    id: str = field(default_factory=lambda: str(uuid.uuid4()))