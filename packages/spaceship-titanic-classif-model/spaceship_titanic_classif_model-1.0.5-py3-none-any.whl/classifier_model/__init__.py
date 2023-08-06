import logging

from classifier_model.config.core import PACKAGE_ROOT, config

logging.getLogger(config.app_config.package_name)

with open(PACKAGE_ROOT / "VERSION", "r") as f:
    __version__ = f.read().strip()
