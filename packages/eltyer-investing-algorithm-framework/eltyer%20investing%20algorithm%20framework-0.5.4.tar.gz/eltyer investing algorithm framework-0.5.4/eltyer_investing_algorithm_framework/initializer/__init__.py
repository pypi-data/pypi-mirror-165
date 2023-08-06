import logging

from eltyer_investing_algorithm_framework.configuration import constants
from investing_algorithm_framework import AlgorithmContextInitializer, \
    AlgorithmContext
from investing_algorithm_framework.core.exceptions import ImproperlyConfigured
from eltyer import Client

logger = logging.getLogger(__name__)


class EltyerInitializer(AlgorithmContextInitializer):

    def initialize(self, algorithm: AlgorithmContext) -> None:
        client = Client()
        client.config.API_KEY = algorithm.config.get(constants.ELTYER_API_KEY)

        if algorithm.config.get_stateless():
            client.start(notify_online=False)
        else:
            client.start()

        environment = client.get_environment()

        if environment is None:
            raise ImproperlyConfigured(
                "Could not retrieve algorithm environment from ELTYER"
            )

        algorithm.config.add(constants.ELTYER_CLIENT, client)
