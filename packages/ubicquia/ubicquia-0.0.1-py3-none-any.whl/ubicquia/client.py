"""Expose client API


"""

# from .alerts import Alerts
from .base import UbicquiaSession
# from .light_control import LightControl
from .nodes import Nodes
from .public_safety import PublicSafety
from .traffic_mobility import TrafficMobility
from .wifi import Wifi


class Ubicquia:
    """API Interface"""
    def __init__(self, session: UbicquiaSession) -> None:
        # self.alerts = Alerts(base_url=BASE_URL, session=session)
        # self.light_control = LightControl(base_url=BASE_URL, session=session)
        self.nodes = Nodes(session)
        self.public_safety = PublicSafety(session)
        self.session = session
        self.traffic_mobility = TrafficMobility(session)
        self.wifi = Wifi(session)
