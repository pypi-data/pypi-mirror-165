from __future__ import annotations

import abc
import logging
import os
import subprocess
import sys
from collections import OrderedDict
from os import path
from typing import Any, Dict, List, Optional, Set, TypeVar, Union

from typing_extensions import Self

_logger_level = getattr(logging, os.environ.get("NDP_SERVER_LOG_LEVEL", "INFO"), logging.INFO)

_logger = logging.getLogger(__name__)
_logger.setLevel(logging.DEBUG)
_logger.addHandler(logging.StreamHandler())


class Dictable(abc.ABC):
    @abc.abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        ...

    @staticmethod
    def clean_config_dict(values: Union[Dict[str, Any], Dictable]) -> Dict[str, str]:
        new_values = OrderedDict()
        if isinstance(values, Dictable):
            values = values.to_dict()

        for key, value in values.items():
            if isinstance(value, dict):
                value = Dictable.clean_config_dict(value)
            elif isinstance(value, (list, tuple, set)):
                value = ",".join([str(x) for x in value]) or ""
            if value is not False and value is not None and not isinstance(value, dict):
                new_values[key] = str(value)
        return new_values

    @staticmethod
    def clean_none_env_vars(dict_value: Union[Dict[str, Any], Dictable]) -> Dict[str, Any]:
        result = OrderedDict()
        if isinstance(dict_value, Dictable):
            dict_value = dict_value.to_dict()

        for key, value in dict_value.items():
            if value is not None:
                result[key] = value
        return result


class ConfigConvert:
    @staticmethod
    def is_true(any: Union[str, bool, int, float, None]) -> bool:
        if not any or not isinstance(any, (str, bool, int)):
            return False
        return bool(any) and (str(any).isdigit() and bool(int(any))) or (str(any).capitalize() == str(True)) or False

    @staticmethod
    def to_int(any: Union[str, bool, int, float, None]) -> int:
        if not any or not isinstance(any, (str, bool, int)):
            return 0
        if isinstance(any, str):
            return any.isdigit() and int(any) or "." in any and int(float(any)) or 0
        return int(any)


class EnvMapper(ConfigConvert, abc.ABC):
    _auto_register = True

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if getattr(cls, "_auto_register", True):
            Registry.mappers.add(cls)

    @abc.abstractmethod
    def map_vars(self, env_vars: Dict[str, str]) -> Dict[str, str]:
        ...

    def get_value(self, env_vars: Dict[str, str], possible_value: List[str], default: str = None) -> Optional[str]:
        for value in possible_value:
            res = env_vars.get(value)
            if res:
                return res
        return default


class OdooConfigABC(ConfigConvert, abc.ABC):
    def __init__(self, main_instance=True):
        super(OdooConfigABC, self).__init__()
        self.main_instance = main_instance

    @property
    @abc.abstractmethod
    def odoo_version(self) -> int:
        ...


def get_odoo_version(env: Dict[str, Any]) -> int:
    return ConfigConvert.to_int(env.get("ODOO_VERSION"))


def is_main_instance(env: Dict[str, Any]) -> bool:
    return ConfigConvert.to_int(env.get("INSTANCE_NUMER")) == 0


OdooCliFlag = Dict[str, Any]


class OdooConfigSection(ConfigConvert, Dictable, abc.ABC):
    _auto_register = True

    def __init__(self, odoo_config_maker: OdooConfigABC) -> None:
        self.config_maker = odoo_config_maker
        self.enable = True
        self.disable_dict = {}

    def to_dict(self) -> Dict[str, Any]:
        if not self.enable:
            return self.disable_dict
        return self._to_flag()

    @abc.abstractmethod
    def _to_flag(self) -> OdooCliFlag:
        ...

    @abc.abstractmethod
    def populate_from_env(self, env_vars: Dict[str, Union[str, bool, int, None]]) -> Self:
        ...

    def __repr__(self) -> str:
        desc = f"{str(self.__class__)}#{id(self)}"
        params = f"{self.enable}, {', '.join([str(i[0]) + '=' + str(i[1]) for i in self.to_dict().items()])}"
        return f"{desc}({params})"

    def __init_subclass__(cls: OdooConfigSection, **kwargs):
        super().__init_subclass__(**kwargs)
        if getattr(cls, "_auto_register", True):
            Registry.sections.add(cls)


class ToOdooArgs(abc.ABC):
    @abc.abstractmethod
    def to_odoo_args(self) -> List[str]:
        ...

    @staticmethod
    def dicatable_to_args(*dictables: Dictable) -> ToOdooArgs:
        result = _ListToOdooArgs()
        for dictable in dictables:
            dict_values = Dictable.clean_none_env_vars(dictable.to_dict())
            dict_values = Dictable.clean_config_dict(dict_values)
            for key, value in dict_values.items():
                if not value:
                    continue
                if value == str(True):
                    result.append(key)
                else:
                    result.append("%s=%s" % (key, value))
        return result


class _ListToOdooArgs(ToOdooArgs, list):
    def to_odoo_args(self) -> List[str]:
        return list(self)


DEFAULT_ODOO_CLI = "ndpserver"

TYPE_LAUNCHER = TypeVar("TYPE_LAUNCHER", bound="AbstractLauncher")


class AbstractLauncher(object):
    _auto_register: bool = True
    _server_mode: str
    _odoo_cli: str = DEFAULT_ODOO_CLI
    _timeout: Optional[int] = None
    server_path = path.join(path.dirname(__file__), "odoo_modules")
    depends: List[TYPE_LAUNCHER] = []

    def __init__(self, *, odoo_path: str = None, odoo_rc: str = None):
        self.odoo_path = path.abspath(path.expanduser(odoo_path))
        self.odoo_rc = path.abspath(path.expanduser(odoo_rc))
        self.ensure_path()

    def ensure_path(self):
        if not path.exists(self.odoo_path) or not path.exists(path.join(self.odoo_path, "odoo-bin")):
            raise FileNotFoundError("File 'odoo-bin' not found in %s" % self.odoo_path)
        if not path.exists(self.server_path):
            raise FileNotFoundError("Directory '%s' not exist" % self.server_path)

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if getattr(cls, "_auto_register", True):
            Registry.launcher.add(cls)

    def normalize_args(self, config: ToOdooArgs) -> List[str]:
        """
        return as a list a valid subprocess.Popen command.
        This commande launch Odoo with the custom command provide by `odoo_cli`
        Args:
             odoo_cli: The odoo cli, like configcreate, customserver, customshell and other
             config: The odoo config to convert to odoo cli arguments
        Return:
            The argument for Popen
        """

        return self._get_python_server_execute() + config.to_odoo_args()

    def execute_odoo_cli(self, config: Optional[ToOdooArgs]) -> subprocess.Popen:
        return self._execute_popen(self.normalize_args(config))

    def _get_python_server_execute(self):
        cmd_args = [sys.executable, path.join(self.odoo_path, "odoo-bin")]
        if self._odoo_cli:
            cmd_args.append("--addons-path=%s" % self.server_path)
            cmd_args.append(self._odoo_cli)
        return cmd_args

    @staticmethod
    def _execute_popen(cmd: List[str]) -> subprocess.Popen:
        _logger.info("Run -> %s", " ".join([str(s) for s in cmd]))
        return subprocess.Popen(cmd)

    @abc.abstractmethod
    def get_config(self, env: Dict[str, str]) -> Optional[ToOdooArgs]:
        ...

    def run_without_config(self, cli: str, *, env: Dict[str, str]) -> int:
        return 0

    def run(self, env: Dict[str, str]) -> int:
        if self.depends:
            _logger.info("Run depends of %s", self)
            for depend_type in self.depends:
                depend = depend_type(odoo_path=self.odoo_path, odoo_rc=self.odoo_rc)
                depend.run(env)
        config = self.get_config(env)
        if not config or not config.to_odoo_args():
            _logger.info("Run without_config %s", self)
            return self.run_without_config(self._odoo_cli, env=env)
        return self.execute_odoo_cli(config).wait(self._timeout)


TYPE_SECTION = TypeVar("TYPE_SECTION", bound=OdooConfigSection)
TYPE_MAPPER = TypeVar("TYPE_MAPPER", bound=EnvMapper)


class _Registry:
    def __init__(self):
        self.sections: Set[TYPE_SECTION] = set()
        self.mappers: Set[TYPE_MAPPER] = set()
        self.launcher: Set[TYPE_LAUNCHER] = set()


Registry = _Registry()
