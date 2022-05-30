from dataclasses import dataclass
from typing import Callable, Optional


@dataclass
class Endpoint:
    """
    - method - the action we want to make. For example get users
    - args - the arguments we want to pass to our method
    - key - unique key for identify our action
    - response - expected response which should be retuned by method.

    Used to annotate common method actions. For example authorization. We have
    a lot of endpoint which we want to check for authorization. And this
    class help us keep all attributes together

    Used dataclass for now. In future we should override it with models manager
    """
    args: tuple
    method: Callable
    key: Optional[str] = None
    response: Optional[int] = None
