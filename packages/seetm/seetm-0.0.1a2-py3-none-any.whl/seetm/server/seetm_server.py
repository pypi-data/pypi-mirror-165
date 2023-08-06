import logging
import os
from typing import Dict

from waitress import serve as waitress_serve

from seetm.server import create_app
from seetm.shared.constants import (
    DEFAULT_PORT,
    DEFAULT_HOST_LOCAL,
    SEETM_ASCII_LOGO,
    ServerEnv, Config,
)
from seetm.shared.exceptions.base import (
    SEETMException,
)
from seetm.shared.exceptions.core import (
    SEETMCoreException
)
from seetm.shared.exceptions.server import (
    SEETMServerException,
    ServerNotFoundException,
)

logger = logging.getLogger(__name__)


class SEETMServer:
    def __init__(
            self,
            configs: Dict,
            debug_mode: bool = False,
    ):
        self.configs = configs
        self.host = configs[Config.SERVER_CONFIGS_KEY][Config.HOST_KEY] or DEFAULT_HOST_LOCAL
        self.port = configs[Config.SERVER_CONFIGS_KEY][Config.PORT_KEY] or DEFAULT_PORT
        self.data_path = configs[Config.BASE_CONFIGS_KEY][Config.DATA_PATH_KEY]
        self.method = configs[Config.BASE_CONFIGS_KEY][Config.METHOD_KEY]
        self.debug_mode = debug_mode

    def run(self) -> None:
        logger.info(f"Starting SEETM server at http://{self.host}:{self.port}/")
        try:
            configs = self.configs
            app_config = {
                "SEETM": configs,
                "APP_THEME": os.environ.get("APP_THEME") or "dark",
                "APP_ENV": os.environ.get("APP_ENV") or "prod",
                "SINHALA_ENABLED": os.environ.get("SINHALA_ENABLED") or True,
            }

            if self.debug_mode:
                logger.warning("Deploying SEETM Server in development mode...")
                os.environ["APP_ENV"] = ServerEnv.DEV
                app = create_app(configs=app_config)
                app.run(
                    host=self.host,
                    port=self.port,
                    debug=self.debug_mode
                )
            else:
                logger.info("Deploying SEETM Server in production mode...")
                print(SEETM_ASCII_LOGO)
                waitress_serve(
                    create_app(configs=app_config),
                    host=self.host,
                    port=self.port
                )

                # # Run as a shell command if required
                # import subprocess
                # subprocess.run(["waitress-serve", f"--host={self.host}",
                #                 f"--port={self.port}", "seetm.server.seetm_server:run"])

        except ServerNotFoundException:
            logger.exception(f"An unknown exception occurred while invoking the SEETMServer")
        except SEETMCoreException:
            logger.exception(f"Core::SEETMServer")
        except SEETMServerException:
            logger.exception(f"Specific::SEETMServer")
        except SEETMException:
            logger.exception(f"Base::SEETMServer")
        except KeyboardInterrupt:
            logger.info(f"Gracefully terminating SEETM Server...")
            exit()
        except OSError:
            logger.exception(f"Possible permission exception while starting the SEETMServer")
        except Exception as e:
            logger.exception(f"Base::broad::SEETMServer. more info: {e}")
        return
