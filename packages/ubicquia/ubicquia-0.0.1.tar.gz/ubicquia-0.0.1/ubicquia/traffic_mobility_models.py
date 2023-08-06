from typing import List
from .base_models import Link, ResponseModel, Meta


class TrafficMobilityResponse(ResponseModel):
    data: List
    meta: Meta
    links: Link
