from typing import Any

class BaseRow:
    def __init__(self, parent, processors, keymap, key_style, data) -> None: ...
    def __reduce__(self): ...
    def __iter__(self): ...
    def __len__(self): ...
    def __hash__(self): ...
    __getitem__: Any

def safe_rowproxy_reconstructor(__cls, __state): ...
