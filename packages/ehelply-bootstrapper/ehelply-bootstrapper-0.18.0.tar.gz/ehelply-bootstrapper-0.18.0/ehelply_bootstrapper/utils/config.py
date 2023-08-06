import os
from typing import List


def load_config(config_path, configs: List[str] = None):
    from ehelply_bootstrapper.utils.state import State
    from pymlconf import Root

    if State.config is None:
        State.config = Root()

    default_configs = [
        '/bootstrap.yaml',
        '/aws.yaml',
        '/fastapi.yaml',
        '/mongo.yaml',
        '/rabbitmq.yaml',
        '/redis.yaml',
        '/sentry.yaml',
        '/sql.yaml',
        '/app.yaml'
    ]

    for default_config in default_configs:
        if os.path.isfile(config_path + default_config):
            configs.append(default_config)

    if configs:
        for config in configs:
            State.config.loadfile(config_path + '/' + config)
