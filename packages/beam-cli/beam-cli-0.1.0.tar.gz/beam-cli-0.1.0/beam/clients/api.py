import requests

from typing import Optional
from beam.constants import (
    REQUESTS_TIMEOUT,
    BACKEND_BASE_URL,
)

TOKEN = "c3a9d1422cc0d4847e02f66ade0e9d4e1174378f45b91e09bde0e49063efddc3b3bb02dee19d4f34a03f0f014a3cfee1ca16409beb3eb1a568675435a4b90b0e"  # TODO: replace with API key based auth


class BeamApiClient:
    @classmethod
    def _post(cls, *, route: str, body):
        body = {k: v for k, v in body.items() if v is not None}
        res = requests.post(
            f"{BACKEND_BASE_URL}/{route}",
            headers={"Authorization": f"identity {TOKEN}"},
            json=body,
            timeout=REQUESTS_TIMEOUT,
        )
        res.raise_for_status()
        return res.json()

    @classmethod
    def down(cls, *, sandbox_id: Optional[str] = None):
        return cls._post(route="sandbox/beam/down", body={"sandbox_id": sandbox_id})

    @classmethod
    def up(cls, *, sandbox_id: Optional[str] = None):
        return cls._post(route="sandbox/beam/up", body={"sandbox_id": sandbox_id})

    @classmethod
    def start(cls, *, sandbox_name: str):
        return cls._post(
            route="sandbox/beam/start", body={"sandbox_name": sandbox_name}
        )

    @classmethod
    def init(cls, *, sandbox_id: Optional[str] = None):
        return cls._post(route="sandbox/beam/init", body={"sandbox_id": sandbox_id})
