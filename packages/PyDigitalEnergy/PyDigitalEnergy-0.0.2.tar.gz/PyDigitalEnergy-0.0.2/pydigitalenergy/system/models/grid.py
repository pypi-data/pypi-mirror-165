from typing import Union, Optional, List


class DockerRegistry:
    def __init__(self, server: str, username: Optional[str] = '', password: Optional[str] = '', **kwargs):
        self.server = server
        self.username = username
        self.password = password
        self.__dict__.update(kwargs)


class Email:
    def __init__(self, enabled: bool, address: Optional[str] = '', **kwargs):
        self.enabled = enabled
        self.address = address
        self.__dict__.update(kwargs)


class HealthCheckNotification:
    def __init__(self, emails: Optional[List[Email]] = [], **kwargs):
        self.emails = [] if not emails else [Email(**email) for email in emails]
        self.__dict__.update(kwargs)


class Net:
    def __init__(self, eRate: Optional[int] = None, inBurst: Optional[int] = None, inRate: Optional[int] = None, **kwargs):
        self.e_rate = eRate
        self.in_burst = inBurst
        self.in_rate = inRate
        self.__dict__.update(kwargs)


class NetQos:
    def __init__(self, ext_net: Union[Net, dict], vins: Union[Net, dict], **kwargs):
        self.ext_net = Net(**ext_net) if isinstance(ext_net, dict) else ext_net
        self.vins = Net(**vins) if isinstance(vins, dict) else vins
        self.__dict__.update(kwargs)


class Prometheus:
    def __init__(self, scrapeInterval: int, **kwargs):
        self.scrape_interval = scrapeInterval
        self.__dict__.update(kwargs)


class Settings:
    def __init__(self, enableUptimeMonitor: bool, allowedports: Optional[List[int]] = [], cleanupRetentionPeriod: Optional[int] = None, docker_registry: Optional[DockerRegistry] = None, extnetMaxPreReservationsNum: Optional[int] = None, healthcheck_notifications: Optional[HealthCheckNotification] = None, limits = None, net_qos: Optional[NetQos] = None, prometheus: Optional[Prometheus] = None, registrationPassword: Optional[str] = '', registrationUrl: Optional[str] = '', registrationUser: Optional[str] = '', vinsMaxPreReservationsNum: Optional[int] = None, vnfdev_mgmt_net_range: Optional[str] = '', **kwargs):
        self.enable_uptime_monitor = enableUptimeMonitor
        self.allowed_ports = allowedports
        self.cleanup_retention_period = cleanupRetentionPeriod
        self.docker_registry = DockerRegistry(**docker_registry) if isinstance(docker_registry, dict) else docker_registry
        self.extnet_max_pre_reservations_num = extnetMaxPreReservationsNum
        self.healthcheck_notifications = HealthCheckNotification(**healthcheck_notifications) if isinstance(healthcheck_notifications, dict) else healthcheck_notifications
        self.limits = limits
        self.net_qos = NetQos(**net_qos) if isinstance(net_qos, dict) else net_qos
        self.prometheus = Prometheus(**prometheus) if isinstance(prometheus, dict) else prometheus
        self.registration_assword = registrationPassword
        self.registration_url = registrationUrl
        self.registration_ser = registrationUser
        self.vins_max_pre_reservations_num = vinsMaxPreReservationsNum
        self.vnfdev_mgmt_net_range = vnfdev_mgmt_net_range
        self.__dict__.update(kwargs)


class Grid:
    def __init__(self, id: int, name: str, guid: Optional[int] = None, nid: Optional[int] = None, settings: Optional[Settings] = None, useavahi: Optional[int] = None, _ckey: Optional[str] = '', **kwargs):
        self.id = id
        self.name = name
        self.guid = guid
        self.nid = nid
        self.settings = Settings(**settings) if isinstance(settings, dict) else settings
        self.useavahi = useavahi
        self._ckey = _ckey
        self.__dict__.update(kwargs)
