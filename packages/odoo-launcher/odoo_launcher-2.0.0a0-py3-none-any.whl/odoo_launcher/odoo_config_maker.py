from __future__ import annotations

import logging
import pprint
from typing import Any, Dict, List, NoReturn, Optional, Type, TypeVar, Union

from . import exceptions
from .api import (
    ConfigConvert,
    Dictable,
    EnvMapper,
    OdooConfigABC,
    OdooConfigSection,
    Registry,
    ToOdooArgs,
    is_main_instance,
)

_logger = logging.getLogger(__name__)
_logger.setLevel(logging.DEBUG)
_logger.addHandler(logging.StreamHandler())

PG_MAX_CONN_MODE_AUTO = "AUTO"
PG_MAX_CONN_MODE_DEFAULT = "DEFAULT"


class OdooConfigFileRef(ToOdooArgs):
    def __init__(self, odoo_rc: str = None):
        self.odoo_rc = odoo_rc

    def to_odoo_args(self) -> List[str]:
        return ["--config=%s" % self.odoo_rc]


T = TypeVar("T", bound="OdooConfigSection")


class OdooConfig(OdooConfigABC, Dictable, ToOdooArgs):
    _sections: Dict[Type[OdooConfigSection], OdooConfigSection]

    def __init__(self, *, odoo_version: int, odoo_rc: str, main_instance: bool = None):
        super(OdooConfig, self).__init__(main_instance)
        self._odoo_version = odoo_version
        self.odoo_rc = odoo_rc
        self._sections = {}
        self.env_converter: Optional[OdooEnvConverter] = None

    def empty(self) -> OdooConfig:
        """
        Helper function, you can create a new instance of OdooConfig, it's exacly the same.
        :return: A new instance of self without any section inside the internal registry.
        """
        return OdooConfig(odoo_version=self.odoo_version, odoo_rc=self.odoo_rc, main_instance=self.main_instance)

    def load_registry(self, registry: Registry) -> NoReturn:
        for section in registry.sections:
            self.add_section(section, force_enable=False)
        self.env_converter = OdooEnvConverter(*[mapper() for mapper in registry.mappers])

    def populate_all_section(
        self, *type_sections: Type[T], env_vars: Dict[str, Union[str, bool, int, None]] = None
    ) -> NoReturn:
        """
        Like `populate_section` but for a list of type
        :param type_sections: An array of  the type of OdooConfigSection wanted
        :param env_vars: The environment variable passed to each section with OdooConfigSection#populate_from_env.
        :return: Nothing
        """
        if not type_sections:
            type_sections = self._sections.keys()
        for type_section in type_sections:
            self.populate_section(type_section, env_vars=env_vars)

    def populate_section(self, type_section: Type[T], *, env_vars: Dict[str, Union[str, bool, int, None]]) -> T:
        """
        Add the asked type of OdooConfigSection to the internal registry.
        Then OdooConfigSection#populate_from_env is call on the instance.

        The `env_vars` is converted with `env_converter` if exist.
        :param type_section:  The type of OdooConfigSection wanted
        :param env_vars: The environment variable passed to OdooConfigSection#populate_from_env.
        :return: The instance of the type asked
        """
        if self.env_converter:
            env_vars = self.env_converter.map_env_vars(env_vars)
        return self.add_section(type_section, force_enable=False).populate_from_env(env_vars)

    def get_section(self, type_section: Type[T]) -> Optional[T]:
        """
        Get the instance for this type inside the registry, None if not exist.

        Info:
        - use `add_section(..)` to add it to the registry.
        - use `__get_item__` if you always want an instance without add it to the registry.

        :param type_section: The type of OdooConfigSection wanted
        :return:  The instance inside the registry, if not found we return `None`.
        """
        return self._sections.get(type_section)

    def __getitem__(self, item: Type[T]) -> T:
        """
        Like `get_section` but if no value exist inside the internal registry we create one and return it.

        The internal registry is not mutated.
        :param item: The type of OdooConfigSection wanted
        :return: The instance inside the registry, otherwise a new one.
        """
        return self.get_section(item) or item(self)

    def add_section(self, type_section: Type[T], *, force_enable: bool = True) -> T:
        """
        Add the asked type of OdooConfigSection to the internal registry.
        We return it as a pointer, so you can mutate the instance directly after this call.

        If this type is already inside the internal registry we return it without replacing it.

        :param type_section: The type of the config section you want to add to the internal registry
        :param force_enable: if set to false the `enable` is not forced to `True`,
        otherwise the value of `enable` is keep unchanged
        :return: The instance of ConfigSection asked
        """
        section = self[type_section]
        if force_enable:
            section.enable = True
        self._sections[type_section] = section
        return section

    def disable_section(self, *type_sections: Type[T]) -> NoReturn:
        """
        If no `type_sections` is provided then all section inside the internal registry is used.

        Disable all sections with `enable=False`.
        :param type_sections: The type of the config section you want to `enable=False`
        """
        if not type_sections:
            type_sections = self._sections.keys()
        for type_section in type_sections:
            self[type_section].enable = False

    @property
    def odoo_version(self) -> int:
        """
        :return:  The Odoo version passed as parameter
        """
        return self._odoo_version

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert all the internal section **enable** to a dict.
        `to_dict` of each section is called.
        If none of the internal section are enabled the an empty dict is returned.
        :return: A dict with all the value of the internal section enable
        """
        result = {"--config": self.odoo_rc}
        any_section_enabled = False
        for section in self._sections.values():
            any_section_enabled = any_section_enabled or section.enable
            result.update(section.to_dict())
        if not any_section_enabled:
            return {}
        return result

    def __repr__(self) -> str:
        return pprint.pformat(self.to_dict())

    def to_odoo_args(self) -> List[str]:
        """
        Allow to convert the `to_dict` to a list of valid argument for the Odoo cli.
        All value are converted.

        @see Dictable.clean_none_env_vars
        @see Dictable.clean_config_dict

        :return: a liste containing all the value a string. The result is should be valid for the odoo cli
        """
        result = []
        dict_values = Dictable.clean_none_env_vars(self.to_dict())
        dict_values = Dictable.clean_config_dict(dict_values)
        for key, value in dict_values.items():
            if not value:
                continue

            if value == str(True):
                result.append(key)
            else:
                result.append("%s=%s" % (key, value))
        return result


class OdooEnvConverter(ConfigConvert):
    def __init__(self, *mappers: EnvMapper):
        self._mappers = mappers

    def map_env_vars(self, env_vars: Dict[str, str]) -> Dict[str, str]:
        result = dict(env_vars)
        for mapper in self._mappers:
            result.update(mapper.map_vars(env_vars))
        for key in dict(result).keys():
            if not result[key]:
                result.pop(key, None)
        return result

    def assert_env(self, env_vars: Dict[str, str]):
        if not self.is_true(env_vars.get("REMOTE_DB", str(True))):
            return
        if (
            not env_vars.get("DB_NAME")
            or not env_vars.get("DB_PORT")
            or not env_vars.get("DB_HOST")
            or not env_vars.get("DB_USER")
            or not env_vars.get("DB_PASSWORD")
        ):
            raise exceptions.MissingDBCredential()

    def create_config_dict(self, env_vars: Dict[str, str]):
        env_vars = self.map_env_vars(env_vars)
        config = OdooConfig(env_vars, is_main_instance(env_vars))
        new_options = config.to_dict()
        new_options = Dictable.clean_config_dict(new_options)
        return new_options
