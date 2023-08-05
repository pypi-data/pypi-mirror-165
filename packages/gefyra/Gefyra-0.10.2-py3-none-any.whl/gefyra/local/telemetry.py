import configparser
import logging
from pathlib import Path

from cli_tracker.sdk import CliTracker
from gefyra.configuration import __VERSION__

logger = logging.getLogger("gefyra")

#########################################################################################
# Telemetry information
# We are collecting anonymous data about the usage of Gefyra as CLI
# All the data we collect is published here: ``
# This data is supposed to help us develop Gefyra and make it a better tool, prioritize
# issues and work on bugs, features and review of pull requests.
# If you do not which to send telemetry data this is totally fine.
# Just opt out via `gefyra telemetry --off`.
#########################################################################################

SENTRY_DSN = "https://a94b0a0194b045f79897f70f9727d299@sentry.unikube.io/3"


class CliTelemetry:
    dir_name = ".gefyra"
    file_name = "config.ini"

    def __init__(self):
        # We're loading / creating a settings file in the home directory.
        home = Path.home()
        gefyra_dir = home / self.dir_name
        if gefyra_dir.exists():
            gefyra_settings_path = gefyra_dir / self.file_name
            if gefyra_settings_path.exists():
                config = self.load_config(str(gefyra_settings_path))
            else:
                config = self.create_config(gefyra_settings_path)
        else:
            config = self.create_config(gefyra_dir / self.file_name)
        try:
            config["telemetry"].getboolean("track")
        except KeyError:
            config = self.create_config(gefyra_dir / self.file_name)

        if config["telemetry"].getboolean("track"):
            self._init_tracker()

    def _init_tracker(self):
        self.tracker = CliTracker(
            application="gefyra",
            dsn=SENTRY_DSN,
            release=__VERSION__,
        )

    def load_config(self, path):
        config = configparser.ConfigParser()
        config.read(path)
        self.path = path
        return config

    def create_config(self, path):
        config = configparser.ConfigParser()
        config["telemetry"] = {"track": "True"}

        output_file = Path(path)
        output_file.parent.mkdir(exist_ok=True, parents=True)

        with open(str(output_file), "w") as config_file:
            config.write(config_file)
        self.path = path
        return config

    def off(self):
        config = configparser.ConfigParser()
        config.read(self.path)
        config["telemetry"]["track"] = "False"
        with open(str(self.path), "w") as config_file:
            config.write(config_file)
        if hasattr(self, "tracker"):
            self.tracker.report_opt_out()
        logger.info("Disabled telemetry.")

    def on(self):
        config = configparser.ConfigParser()
        config.read(self.path)
        config["telemetry"]["track"] = "True"
        with open(str(self.path), "w") as config_file:
            config.write(config_file)
        self._init_tracker()
        self.tracker.report_opt_in()
        logger.info("Enabled telemetry.")
