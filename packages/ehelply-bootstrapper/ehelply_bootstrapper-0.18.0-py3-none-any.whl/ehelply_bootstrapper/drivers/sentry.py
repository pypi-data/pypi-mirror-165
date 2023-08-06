from ehelply_bootstrapper.drivers.driver import Driver
from ehelply_bootstrapper.utils.state import State
from ehelply_bootstrapper.utils.service import ServiceMeta
from ehelply_bootstrapper.utils.environment import Environment
from ehelply_logger.Logger import VERBOSITY_DEBUG
import sentry_sdk


class Sentry(Driver):
    def __init__(
            self,
            service_meta: ServiceMeta,
            service_process: str,
            verbosity: int = 0,
            sql_alchemy: bool = False
    ):
        self.service_meta: ServiceMeta = service_meta
        self.service_process: str = service_process
        self.sql_alchemy = sql_alchemy

        self.trace_rate: float = 0.1

        if Environment.is_dev():
            self.trace_rate = 1.0
        elif Environment.is_test():
            self.trace_rate = 0.5

        super().__init__(verbosity=verbosity)

    def setup(self):
        integrations: list = []

        sentry_sdk.init(
            State.config.sentry.dsn,
            environment=Environment.stage(),
            release=self.service_meta.key + '@' + self.service_meta.version,
            server_name=self.service_process,
            debug=Environment.is_dev() and self.verbosity >= VERBOSITY_DEBUG,
            integrations=integrations,
            traces_sample_rate=self.trace_rate
        )

        with sentry_sdk.configure_scope() as scope:
            scope.set_tag("service-name", self.service_meta.name)
            scope.set_tag("service-key", self.service_meta.key)
