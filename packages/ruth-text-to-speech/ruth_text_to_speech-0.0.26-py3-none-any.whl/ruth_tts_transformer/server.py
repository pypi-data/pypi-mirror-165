from typing import Dict

from ray import serve
from starlette.requests import Request


@serve.deployment(route_prefix="/")
class MyModelDeployment:
    def __init__(self, msg: str):
        # Initialize model state: could be very large neural net weights.
        self._msg = msg

    def __call__(self, request: Request) -> Dict:
        return {"result": self._msg}


dep = MyModelDeployment.bind(msg="Hello world!")
