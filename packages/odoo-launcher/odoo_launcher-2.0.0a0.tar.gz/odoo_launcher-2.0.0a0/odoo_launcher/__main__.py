import dataclasses
import logging
import os
import pprint
import random
import string
import subprocess
import sys

from . import launcher

_logger = logging.getLogger(__name__)


def get_random_string(length):
    return "".join(random.choice(string.ascii_lowercase) for _ in range(length))


@dataclasses.dataclass
class _Config:
    mode: launcher.OdooMode
    config: str
    odoo_path: str


def _main_parse_args() -> _Config:
    custom_mode = (os.getenv("ODOO_SERVER_MODE") or "").upper()
    if not custom_mode or custom_mode not in launcher.OdooMode.__members__.keys():
        custom_mode = launcher.OdooMode.ODOO.name
    mode = launcher.OdooMode[custom_mode]
    config = os.getenv("ODOO_RC") or os.path.join("/tmp", "odoo_config_%s.ini" % get_random_string(5))
    odoo_path = os.getenv("ODOO_PATH", "/odoo")
    return _Config(mode=mode, config=config, odoo_path=odoo_path)


def _report_env(env):
    _logger.debug("################## ENVIRON ###########################")
    _logger.debug(pprint.pformat(env))
    _logger.debug("################## ENVIRON ###########################")


def main() -> int:
    environ = dict(os.environ)
    config = _main_parse_args()
    _logger.info("Starting Odoo in %s mode", config.mode.value)

    _logger.info("#############################################")
    _logger.info("1/ Install extra addons")
    launcher.AddonsInstallerLauncher(odoo_path=config.odoo_path, odoo_rc=config.config).run(environ)

    # _logger.info("#############################################")
    # _logger.info("2/ Create config file %s", config.config)
    # to_launch = launcher.ConfigLauncher(odoo_path=config.odoo_path, odoo_rc=config.config)
    # return_code = to_launch.run(environ)
    # if return_code:
    #     return return_code

    if config.mode == launcher.OdooMode.CONFIG:
        launcher.ConfigPrinterLauncher(odoo_path=config.odoo_path, odoo_rc=config.config).run(environ)
        return 0

    if config.mode == launcher.OdooMode.TESTS:
        maintenance_server_proc = subprocess.Popen([sys.executable, "-m", "maintenance_server"])
        to_launch = launcher.TestLauncher(odoo_path=config.odoo_path, odoo_rc=config.config)
        return_code = to_launch.run(environ)
        maintenance_server_proc.kill()
        if return_code:
            return return_code

    if config.mode == launcher.OdooMode.WEB:
        return launcher.WebLauncher(odoo_path=config.odoo_path, odoo_rc=config.config).run(environ)

    if config.mode == launcher.OdooMode.UPDATE:
        maintenance_server_proc = subprocess.Popen([sys.executable, "-m", "maintenance_server"])
        to_launch = launcher.UpdateLauncher(odoo_path=config.odoo_path, odoo_rc=config.config)
        return_code = to_launch.run(environ)
        maintenance_server_proc.kill()
        if return_code:
            return return_code

    if config.mode == launcher.OdooMode.INSTALL:
        maintenance_server_proc = subprocess.Popen([sys.executable, "-m", "maintenance_server"])
        to_launch = launcher.InstallLauncher(odoo_path=config.odoo_path, odoo_rc=config.config)
        return_code = to_launch.run(environ)
        maintenance_server_proc.kill()
        if return_code:
            return return_code

    if config.mode == launcher.OdooMode.CONSOLE:
        _logger.info("#############################################")
        _logger.info("NOT SUPPORTED, SORRY :-(")
        _logger.info("#############################################")
        return 1


if __name__ == "__main__":
    handler = logging.StreamHandler()
    _logger.addHandler(handler)
    _logger.setLevel(logging.DEBUG)
    sys.exit(main())
