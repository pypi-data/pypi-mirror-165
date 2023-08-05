import enum
from typing import Dict, Optional, Union

from addons_installer import addons_installer
from typing_extensions import Self

from .api import ConfigConvert, OdooCliFlag, OdooConfigABC, OdooConfigSection


class TestOdooConfigSection(OdooConfigSection):
    def __init__(self, odoo_config_maker: OdooConfigABC) -> None:
        super().__init__(odoo_config_maker)
        self.disable_dict = {"--test-enable": False}
        self.enable = False
        self.test_tags = None
        self.test_file = None

    def populate_from_env(self, env_vars: Dict[str, Union[str, bool, int, None]]) -> Self:
        self.enable = self.is_true(env_vars.get("TEST_ENABLE"))
        self.test_tags = env_vars.get("TEST_TAGS")
        self.test_file = env_vars.get("TEST_FILE")
        return self

    def _to_flag(self) -> OdooCliFlag:
        result = {
            "--test-enable": True,
        }
        if self.test_tags and self.config_maker.odoo_version >= 12:
            result["--test-tags"] = self.test_tags
        if self.test_file:
            result["--test-file"] = self.test_file
        return result


class WorkersOdooConfigSection(OdooConfigSection):
    class UseCase(enum.Enum):
        CLASSIC = "CLASSIC"
        THREADED_MODE = "THREADED_MODE"
        ONLY_HTTP = "ONLY_HTTP"
        ONLY_JOB_RUNNER = "ONLY_JOB_RUNNER"
        ONLY_JOB_WORKER = "ONLY_JOB_WORKER"
        ONLY_CRON = "ONLY_CRON"

    def __init__(self, odoo_config_maker: OdooConfigABC) -> None:
        super().__init__(odoo_config_maker)
        self.http = 1
        self.cron = 2
        self.job = 0
        self.odoo_use_case = WorkersOdooConfigSection.UseCase.CLASSIC

    def populate_from_env(self, env_vars: Dict[str, Union[str, bool, int, None]]) -> Self:
        self.http = ConfigConvert.to_int(env_vars.get("WORKER_HTTP", 1))
        self.cron = ConfigConvert.to_int(env_vars.get("WORKER_CRON", 2))
        self.job = ConfigConvert.to_int(env_vars.get("WORKER_JOB", 0))
        use_case_env = env_vars.get("ODOO_USE_CASE")
        if not use_case_env or use_case_env not in (list(WorkersOdooConfigSection.UseCase)):
            odoo_use_case = WorkersOdooConfigSection.UseCase.CLASSIC
        else:
            odoo_use_case = WorkersOdooConfigSection.UseCase[use_case_env]

        if not self.config_maker.main_instance and odoo_use_case != WorkersOdooConfigSection.UseCase.ONLY_CRON:
            self.cron = 0
        return self

    @property
    def total(self):
        return self.http + self.cron + self.job

    @property
    def worker(self):
        if self.odoo_use_case == WorkersOdooConfigSection.UseCase.THREADED_MODE:
            return 0
        if self.odoo_use_case == WorkersOdooConfigSection.UseCase.ONLY_JOB_WORKER:
            return self.job
        if self.odoo_use_case == WorkersOdooConfigSection.UseCase.ONLY_JOB_RUNNER:
            return 0
        if self.odoo_use_case == WorkersOdooConfigSection.UseCase.ONLY_HTTP:
            return self.http
        if self.odoo_use_case == WorkersOdooConfigSection.UseCase.ONLY_CRON:
            return 0
        return self.http + self.job

    def _to_flag(self) -> OdooCliFlag:
        return {
            "--workers": self.worker,
            "--max-cron-threads": self.cron,
        }


class LimitOdooConfigSection(OdooConfigSection):
    def __init__(self, odoo_config_maker: OdooConfigABC) -> None:
        super().__init__(odoo_config_maker)
        self.limit_request = 0
        self.limit_time_cpu = 0
        self.limit_time_real = 0
        self.osv_memory_count_limit = 0
        self.osv_memory_age_limit = 0
        self.limit_memory_hard = 0
        self.limit_memory_soft = 0

    def populate_from_env(self, env_vars: Dict[str, Union[str, bool, int, None]]) -> Self:
        self.limit_request = int(env_vars.get("LIMIT_REQUEST", 0)) or None
        self.limit_time_cpu = int(env_vars.get("LIMIT_TIME_CPU", 0)) or None
        self.limit_time_real = int(env_vars.get("LIMIT_TIME_REAL", 0)) or None
        self.osv_memory_count_limit = int(env_vars.get("OSV_MEMORY_COUNT_LIMIT", 0)) or None
        self.osv_memory_age_limit = int(env_vars.get("OSV_MEMORY_AGE_LIMIT", 0)) or None
        self.limit_memory_hard = int(env_vars.get("LIMIT_MEMORY_HARD", 0)) or None
        self.limit_memory_soft = int(env_vars.get("LIMIT_MEMORY_SOFT", 0)) or None

        if not self.limit_memory_hard or not self.limit_memory_soft:
            global_limit_memory_hard = int(env_vars.get("GLOBAL_LIMIT_MEMORY_HARD", 0))
            global_limit_memory_soft = int(env_vars.get("GLOBAL_LIMIT_MEMORY_SOFT", 0))
            worker_section = WorkersOdooConfigSection(self.config_maker)
            worker_section.populate_from_env(env_vars)
            nb_workers = worker_section.total or 1
            if not self.limit_memory_soft and global_limit_memory_soft:
                self.limit_memory_soft = global_limit_memory_soft // nb_workers
            if not self.limit_memory_hard and global_limit_memory_hard:
                self.limit_memory_hard = global_limit_memory_hard // nb_workers
        return self

    def _to_flag(self) -> OdooCliFlag:
        return {
            "--limit-request": self.limit_request,
            "--limit-time-cpu": self.limit_time_cpu,
            "--limit-time-real": self.limit_time_real,
            "--limit-memory-hard": self.limit_memory_hard,
            "--limit-memory-soft": self.limit_memory_soft,
            "--osv-memory-count-limit": self.osv_memory_count_limit,
            "--osv-memory-age-limit": self.osv_memory_age_limit,
        }


class DatabaseOdooConfigSection(OdooConfigSection):
    class MaxConnMode(enum.Enum):
        AUTO = "AUTO"
        FIXED = "FIXED"

    def __init__(self, odoo_config_maker: OdooConfigABC) -> None:
        super().__init__(odoo_config_maker)
        self.name = None
        self.host = None
        self.port = None
        self.user = None
        self.password = None
        self.max_conn = 0
        self.filter = None
        self.log_enable = False
        self.log_level = None
        self.show = False

    def populate_from_env(self, env_vars: Dict[str, Union[str, bool, int, None]]) -> Self:
        self.name = env_vars.get("DB_NAME")
        self.host = env_vars.get("DB_HOST")
        self.port = ConfigConvert.to_int(env_vars.get("DB_PORT")) or None
        self.user = env_vars.get("DB_USER")
        self.password = env_vars.get("DB_PASSWORD")
        self.max_conn = ConfigConvert.to_int(env_vars.get("DB_MAX_CONN"))
        self.filter = env_vars.get("DB_FILTER")
        self.log_enable = env_vars.get("LOG_DB")
        self.log_level = env_vars.get("LOG_DB_LEVEL")
        self.show = self.is_true(env_vars.get("LIST_DB"))

        mode = self._get_conn_mode(env_vars)
        if mode == DatabaseOdooConfigSection.MaxConnMode.FIXED and not self.max_conn:
            # Switch to auto if no max_conn in env_vars but in mode FIXED
            mode = DatabaseOdooConfigSection.MaxConnMode.AUTO

        worker_section = WorkersOdooConfigSection(self.config_maker)
        worker_section.populate_from_env(env_vars)
        nb_workers = worker_section.total or 1
        min_conn = nb_workers + int(nb_workers // 2)

        if mode == DatabaseOdooConfigSection.MaxConnMode.AUTO and not self.max_conn:
            # We add some security because sometime worker open 2 or more connecions (Ex :bus.bus)
            self.max_conn = max(self.max_conn, min_conn, 2)

        if self.filter and not self.show:
            self.show = True
        if self.name and not self.show:
            self.filter = self.name
        if self.name and self.show and not self.filter:
            self.filter = self.name + ".*"

        if not self.host or not self.name or not self.user or not self.password:
            self.enable = False
        return self

    def _get_conn_mode(self, env_vars):
        mode_env = env_vars.get("DB_MAX_CONN_MODE")
        if not mode_env or mode_env not in (
            DatabaseOdooConfigSection.MaxConnMode.FIXED.value,
            DatabaseOdooConfigSection.MaxConnMode.AUTO.value,
        ):
            mode = DatabaseOdooConfigSection.MaxConnMode.AUTO
        else:
            mode = DatabaseOdooConfigSection.MaxConnMode[mode_env]
        return mode

    def _to_flag(self) -> OdooCliFlag:
        res = {
            "--db_host": self.host,
            "--db_port": self.port,
            "--db_user": self.user,
            "--db_password": self.password,
            "--database": self.name,
            "--no-database-list": not self.show,
            "--db_maxconn": self.max_conn,
            "--db-filter": self.filter,
        }
        return res


class HttpOdooConfigSection(OdooConfigSection):
    def __init__(self, odoo_config_maker: OdooConfigABC) -> None:
        super().__init__(odoo_config_maker)
        self.enable = True
        self.key_http = "http" if self.config_maker.odoo_version > 10 else "xmlrpc"
        self.disable_dict = {"--no-%s" % self.key_http: True}
        self.interface = "0.0.0.0"
        self.port = 8080
        self.longpolling_port = 4040

    def populate_from_env(self, env_vars: Dict[str, Union[str, bool, int, None]]) -> Self:
        self.enable = self.is_true(env_vars.get("HTTP_ENABLE", "True"))
        self.interface = None
        self.port = None
        self.longpolling_port = None
        self.disable_dict = {"--no-%s" % self.key_http: True}
        if self.enable:
            self.interface = env_vars.get("HTTP_INTERFACE") or "0.0.0.0"
            self.port = ConfigConvert.to_int(env_vars.get("HTTP_PORT")) or 8080
            self.longpolling_port = ConfigConvert.to_int(env_vars.get("LONGPOLLING_PORT")) or 4040
        return self

    def _to_flag(self) -> OdooCliFlag:
        res = {}
        res["--%s-interface" % self.key_http] = self.interface
        res["--%s-port" % self.key_http] = self.port
        res["--longpolling-port"] = self.longpolling_port
        return res


class ServerWideModuleConfigSection(OdooConfigSection):
    def __init__(self, odoo_config_maker: OdooConfigABC) -> None:
        super().__init__(odoo_config_maker)
        self.server_wide_modules = ["base", "web"]
        self.queue_job_module_name = "queue_job"
        if self.config_maker.odoo_version < 10:
            self.queue_job_module_name = "connector"

    def populate_from_env(self, env_vars: Dict[str, Union[str, bool, int, None]]) -> Self:
        str_server_wide_modules = env_vars.get("SERVER_WIDE_MODULES")
        self.server_wide_modules = str_server_wide_modules and str_server_wide_modules.split(",") or ["base", "web"]
        if env_vars.get("QUEUE_JOB_ENABLE"):
            self.server_wide_modules.append(self.queue_job_module_name)
        if self.is_true(env_vars.get("S3_FILESTORE_ENABLE")):
            self.server_wide_modules.append("odoo_filestore_s3")
        if self.is_true(env_vars.get("REDIS_SESSION_ENABLE")):
            self.server_wide_modules.append("odoo_session_redis")
        return self

    def _to_flag(self) -> OdooCliFlag:
        return {
            "--load": self.server_wide_modules,
        }


class MiscSection(OdooConfigSection):
    def __init__(self, odoo_config_maker: OdooConfigABC):
        super(MiscSection, self).__init__(odoo_config_maker)
        self.disable_dict = {"--unaccent": False}
        self.enable = True
        self.unaccent = False
        self.without_demo: Optional[str] = "all"
        self.stop_after_init = False
        self.save_config_file = False
        self.force_stop_after_init = False
        self.force_save_config_file = False

    def populate_from_env(self, env_vars: Dict[str, Union[str, bool, int, None]]) -> Self:
        self.unaccent = self.is_true(env_vars.get("UNACCENT", True))
        self.without_demo = env_vars.get("WITHOUT_DEMO", "all")
        self.stop_after_init = self.is_true(env_vars.get("STOP_AFTER_INIT"))
        self.save_config_file = self.is_true(env_vars.get("SAVE_CONFIG_FILE"))
        return self

    def _to_flag(self) -> OdooCliFlag:
        flags = {}
        if self.unaccent:
            flags["--unaccent"] = self.unaccent
        if isinstance(self.without_demo, str):
            flags["--without-demo"] = self.without_demo
        elif self.without_demo is None:
            flags["--without-demo"] = str(False)
        if self.save_config_file or self.force_save_config_file:
            flags["--save"] = True
        if self.stop_after_init or self.force_stop_after_init:
            flags["--stop-after-init"] = True
        return flags


class LoggerSection(OdooConfigSection):
    def __init__(self, odoo_config_maker: OdooConfigABC) -> None:
        super().__init__(odoo_config_maker)
        self.logfile = None
        self.log_handler = None
        self.log_request = False
        self.log_response = False
        self.log_web = False
        self.log_sql = False
        self.log_db = False
        self.log_db_level = False
        self.log_level = False

    def populate_from_env(self, env_vars: Dict[str, Union[str, bool, int, None]]):
        self.logfile = env_vars.get("LOGFILE")
        self.log_handler = env_vars.get("LOG_HANDLER")
        self.log_request = self.is_true(env_vars.get("LOG_REQUEST"))
        self.log_response = self.is_true(env_vars.get("LOG_RESPONSE"))
        self.log_web = self.is_true(env_vars.get("LOG_WEB"))
        self.log_sql = self.is_true(env_vars.get("LOG_SQL"))
        self.log_db = self.is_true(env_vars.get("LOG_DB"))
        self.log_db_level = env_vars.get("LOG_DB_LEVEL")
        self.log_level = env_vars.get("LOG_LEVEL")

    def _to_flag(self) -> OdooCliFlag:
        flags = {}
        if self.log_level:
            flags["--logfile"] = self.logfile
        if self.log_handler:
            flags["--log-handler"] = self.log_handler
        if self.log_request:
            flags["--log-request"] = self.log_request
        if self.log_response:
            flags["--log-response"] = self.log_response
        if self.log_web:
            flags["--log-web"] = self.log_web
        if self.log_sql:
            flags["--log-sql"] = self.log_sql
        if self.log_db:
            flags["--log-db"] = self.log_db
        if self.log_db_level:
            flags["--log-db-level"] = self.log_db_level
        if self.log_level:
            flags["--log-level"] = self.log_level
        return flags


class UpdateInstallSection(OdooConfigSection):
    def __init__(self, odoo_config_maker: OdooConfigABC) -> None:
        super().__init__(odoo_config_maker)
        self.enable = False
        self.update = []
        self.install = []

    def populate_from_env(self, env_vars: Dict[str, Union[str, bool, int, None]]) -> Self:
        self.update = [u.strip() for u in (env_vars["UPDATE"]).split(",")] if env_vars.get("UPDATE") else []
        self.install = [i.strip() for i in env_vars["INSTALL"].split(",")] if env_vars.get("INSTALL") else []
        return self

    def _to_flag(self) -> OdooCliFlag:
        flags = {}
        if self.update:
            flags["--update"] = ",".join(self.update)
        if self.install:
            flags["--init"] = ",".join(self.install)
        return flags


class AddonsPathConfigSection(OdooConfigSection):
    def __init__(self, odoo_config_maker: OdooConfigABC):
        super(AddonsPathConfigSection, self).__init__(odoo_config_maker)
        self.registry = addons_installer.AddonsFinder()
        self.addons_path = []

    def populate_from_env(self, env_vars: Dict[str, Union[str, bool, int, None]]) -> Self:
        result = self.registry.parse_env(env_vars=env_vars)
        self.addons_path = [r.addons_path for r in result]
        return self

    def _to_flag(self) -> OdooCliFlag:
        return {
            "--addons-path": self.addons_path,
        }
