from __future__ import annotations

import configparser
import enum
import io
import logging
import os
import sys
import uuid
from os import path
from typing import Dict, Optional

from addons_installer import AddonsFinder, AddonsInstaller

from . import api, exceptions
from .config_section import (
    HttpOdooConfigSection,
    LoggerSection,
    MiscSection,
    TestOdooConfigSection,
    UpdateInstallSection,
    WorkersOdooConfigSection,
)
from .odoo_config_maker import OdooConfig, OdooConfigFileRef

_logger = logging.getLogger("launch")
_logger.setLevel(logging.DEBUG)
_logger.addHandler(logging.StreamHandler())

_logger.debug("Warning options %s", sys.warnoptions)
if not sys.warnoptions:
    import warnings

    warnings.simplefilter("module", SyntaxWarning)  # Change the filter in this process
    warnings.simplefilter("ignore", category=DeprecationWarning)
    os.environ["PYTHONWARNINGS"] = "ignore"  # Also affect subprocesses


@enum.unique
class OdooMode(enum.Enum):
    # enum.auto() not available in enum34 compatibility package for py2.7
    WEB = "WEB"
    TESTS = "TESTS"
    CONSOLE = "CONSOLE"
    CONFIG = "CONFIG"
    INSTALL = "INSTALL"
    UPDATE = "UPDATE"


class ConfigLauncher(api.AbstractLauncher):
    _odoo_cli = "configcreate"

    def clean_workdir(self) -> None:
        if path.exists(self.odoo_rc):
            os.remove(self.odoo_rc)

    def get_config(self, env: Dict[str, str]) -> Optional[OdooConfig]:
        config = OdooConfig(
            odoo_rc=self.odoo_rc, odoo_version=api.get_odoo_version(env), main_instance=api.is_main_instance(env)
        )
        _logger.info("Apply registry")
        config.load_registry(api.Registry)
        try:
            _logger.info("Populate config from env")
            config.populate_all_section(env_vars=env)
            config[TestOdooConfigSection].enable = False
        except exceptions.OdooLauncherException as e:
            _logger.exception("Error before boot odoo", exc_info=e)
            return config.empty()

        if not path.exists(self.odoo_rc):
            config[MiscSection].save_config_file = True
        return config

    def run(self, env: Dict[str, str]) -> int:
        return_code = super(ConfigLauncher, self).run(env)
        if not return_code:
            self._apply_hard_coded_conf()
        return return_code

    def _apply_hard_coded_conf(self, parser=None, save=True):
        if not os.path.exists(self.odoo_rc):
            return
        default_config = parser
        if not parser:
            default_config = configparser.ConfigParser()
            default_config.read(self.odoo_rc)
        default_config.set("options", "admin_passwd", os.environ.get("ADMIN_PASSWD", str(uuid.uuid4())))
        default_config.set("options", "csv_internal_sep", os.environ.get("CSV_INTERNAL_SEP", ","))
        default_config.set("options", "publisher_warranty_url", "https://ndp-systemes.fr")
        default_config.set("options", "reportgz", str(False))
        default_config.set("options", "root_path", str(False))
        if save:
            with io.open(self.odoo_rc, "w") as file:
                default_config.write(file)


class AddonsInstallerLauncher(api.AbstractLauncher):
    def _install_addons(self, env_vars: Dict[str, str]):
        addons = AddonsFinder.parse_env(env_vars)
        for addon in addons:
            AddonsInstaller.install(addon)

    def run(self, env: Dict[str, str]) -> int:
        self._install_addons(env)
        return 0


class TestLauncher(api.AbstractLauncher):
    def get_config(self, env: Dict[str, str]) -> OdooConfig:
        config = OdooConfig(
            odoo_rc=self.odoo_rc, odoo_version=api.get_odoo_version(env), main_instance=api.is_main_instance(env)
        )

        section = config.populate_section(TestOdooConfigSection, env_vars=env)
        install_section = config.populate_section(UpdateInstallSection, env_vars=env)

        if not install_section.install and not (config.odoo_version >= 12 and section.test_tags):
            return config.empty()

        section.enable = True
        install_section.enable = True

        logger_section = config.add_section(LoggerSection)
        logger_section.log_level = "test"

        misc_section = config.add_section(MiscSection)
        misc_section.enable = True
        misc_section.unaccent = True
        misc_section.force_stop_after_init = True
        misc_section.without_demo = None  # We fore to None so --without-demo=False is passed to cli

        # Ensure disable worker a move to threaded mode
        worker_section = config.add_section(WorkersOdooConfigSection)
        worker_section.odoo_use_case = WorkersOdooConfigSection.UseCase.THREADED_MODE
        worker_section.cron = 0
        return config

    def run_without_config(self, cli: str, *, env: Dict[str, str]) -> int:
        _logger.info(
            """No Test to run.
please add TEST_ENABLE=True
and TEST_MODULE, or TEST_TAGS with a value
"""
        )
        return 2


class InstallLauncher(api.AbstractLauncher):
    depends = [ConfigLauncher]

    def get_config(self, env: Dict[str, str]) -> OdooConfig:
        config = OdooConfig(
            odoo_rc=self.odoo_rc, odoo_version=api.get_odoo_version(env), main_instance=api.is_main_instance(env)
        )
        section = config.populate_section(UpdateInstallSection, env_vars=env)
        section.enable = True

        misc_section = config.populate_section(MiscSection, env_vars=env)
        misc_section.force_stop_after_init = True

        web_section = config.add_section(HttpOdooConfigSection)
        web_section.enable = False
        return config


class UpdateLauncher(InstallLauncher):
    depends = [ConfigLauncher]

    def get_config(self, env: Dict[str, str]) -> OdooConfig:
        config = super(UpdateLauncher, self).get_config(env)
        config[UpdateInstallSection].install = None
        return config


class WebLauncher(api.AbstractLauncher):
    depends = [ConfigLauncher]

    def get_config(self, env: Dict[str, str]) -> OdooConfigFileRef:
        return OdooConfigFileRef(self.odoo_rc)

    def run(self, env: Dict[str, str]) -> int:
        _logger.info("Starting Odoo")
        return super(WebLauncher, self).run(env)


class ConfigPrinterLauncher(api.AbstractLauncher):
    depends = [ConfigLauncher]

    def get_config(self, env: Dict[str, str]) -> Optional[api.ToOdooArgs]:
        return None

    def run_without_config(self, cli: str, *, env: Dict[str, str]) -> int:
        if not path.exists(self.odoo_rc):
            _logger.info(f"No Generated File from environement stored in {self.odoo_rc}")
            return 1

        _logger.info(f"Generated File from environement stored in {self.odoo_rc}")
        default_config = configparser.ConfigParser()
        default_config.read(self.odoo_rc)

        _logger.info("==========================================================")
        for section in default_config.sections():
            _logger.info(f"[{section}]")
            for key in default_config.options(section):
                _logger.info(f"{key} = {default_config.get(section, key)}")
        _logger.info("==========================================================")
        return 0
