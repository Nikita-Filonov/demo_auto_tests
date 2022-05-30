from pathlib import Path
from typing import AnyStr, Union
from uuid import UUID

PathLike = Union[str, AnyStr, Path]
EntityId = Union[str, UUID]
