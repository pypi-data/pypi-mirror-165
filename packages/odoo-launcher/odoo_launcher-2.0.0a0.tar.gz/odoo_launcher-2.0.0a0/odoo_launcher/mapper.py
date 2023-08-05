from typing import Dict, Union

from .api import EnvMapper


class OdooCompatibilityMapper(EnvMapper):
    """
    <WORKER_HTTP> is put in <WORKERS> if <WORKERS> not exist
    and
    <WORKERS> is put in <WORKER_HTTP> if <WORKER_HTTP> not exist
    """

    def map_vars(self, env_vars):
        # type: (Dict[str, str]) -> Dict[str, str]
        return {
            "WORKER_HTTP": self.get_value(env_vars, ["WORKER_HTTP", "WORKERS"]),
            "WORKER_CRON": self.get_value(env_vars, ["WORKER_CRON", "WORKERS"]),
            "WORKER_JOB": self.get_value(env_vars, ["WORKER_JOB", "WORKERS"]),
            "HTTP_INTERFACE": self.get_value(env_vars, ["HTTP_INTERFACE", "XMLRPC_INTERFACE"]),
            "HTTP_PORT": self.get_value(env_vars, ["HTTP_PORT", "XMLRPC_PORT"]),
            "HTTP_ENABLE": self.get_value(env_vars, ["HTTP_ENABLE", "XMLRPC_ENABLE"]),
            "LONGPOLLING_PORT": self.get_value(env_vars, ["LONGPOLLING_PORT"]),
            "SERVER_WIDE_MODULES": self.get_value(env_vars, ["SERVER_WIDE_MODULES", "LOAD"]),
        }


class OdooQueueJobMapper(EnvMapper):
    """
    <WORKER_HTTP> is put in <WORKERS> if <WORKERS> not exist
    and
    <WORKERS> is put in <WORKER_HTTP> if <WORKER_HTTP> not exist
    """

    def map_vars(self, env_vars):
        # type: (Dict[str, str]) -> Dict[str, str]
        enable = self.is_true(env_vars.get("ODOO_QUEUE_JOB_ENABLE"))
        return {
            "ODOO_QUEUE_JOB_ENABLE": str(enable),
            "ODOO_QUEUE_JOB_CHANNELS": enable
            and self.get_value(env_vars, ["ODOO_QUEUE_JOB_CHANNELS", "ODOO_CONNECTOR_CHANNELS"])
            or None,
            "ODOO_QUEUE_JOB_SCHEME": enable
            and self.get_value(env_vars, ["ODOO_QUEUE_JOB_SCHEME", "ODOO_CONNECTOR_SCHEME"])
            or None,
            "ODOO_QUEUE_JOB_HOST": enable
            and self.get_value(env_vars, ["ODOO_QUEUE_JOB_HOST", "ODOO_CONNECTOR_HOST"])
            or None,
            "ODOO_QUEUE_JOB_PORT": enable
            and self.get_value(env_vars, ["ODOO_QUEUE_JOB_PORT", "ODOO_CONNECTOR_PORT"])
            or None,
            "ODOO_QUEUE_JOB_HTTP_AUTH_USER": enable
            and self.get_value(env_vars, ["ODOO_QUEUE_JOB_HTTP_AUTH_USER", "ODOO_CONNECTOR_HTTP_AUTH_USER"])
            or None,
            "ODOO_QUEUE_JOB_HTTP_AUTH_PASSWORD": enable
            and self.get_value(env_vars, ["ODOO_QUEUE_JOB_HTTP_AUTH_PASSWORD", "ODOO_CONNECTOR_HTTP_AUTH_PASSWORD"])
            or None,
            "ODOO_QUEUE_JOB_JOBRUNNER_DB_HOST": enable
            and self.get_value(env_vars, ["ODOO_QUEUE_JOB_JOBRUNNER_DB_HOST", "ODOO_CONNECTOR_JOBRUNNER_DB_HOST"])
            or None,
            "ODOO_QUEUE_JOB_JOBRUNNER_DB_PORT": enable
            and self.get_value(env_vars, ["ODOO_QUEUE_JOB_JOBRUNNER_DB_PORT", "ODOO_CONNECTOR_JOBRUNNER_DB_PORT"])
            or None,
        }


class OdooRedisSessionMapper(EnvMapper):
    """
    <WORKER_HTTP> is put in <WORKERS> if <WORKERS> not exist
    and
    <WORKERS> is put in <WORKER_HTTP> if <WORKER_HTTP> not exist
    """

    def map_vars(self, env_vars):
        # type: (Dict[str, str]) -> Dict[str, str]
        enable = self.is_true(
            env_vars.get("REDIS_SESSION_ENABLE", bool(self.get_value(env_vars, ["REDIS_SESSION_HOST", "REDIS_HOST"])))
        )
        return {
            "REDIS_SESSION_ENABLE": str(enable),
            "REDIS_SESSION_URL": enable and self.get_value(env_vars, ["REDIS_SESSION_URL", "REDIS_URL"]) or None,
            "REDIS_SESSION_HOST": enable and self.get_value(env_vars, ["REDIS_SESSION_HOST", "REDIS_HOST"]) or None,
            "REDIS_SESSION_PORT": enable and self.get_value(env_vars, ["REDIS_SESSION_PORT", "REDIS_PORT"]) or None,
            "REDIS_SESSION_DB_INDEX": enable
            and self.get_value(env_vars, ["REDIS_SESSION_DB_INDEX", "REDIS_DB_INDEX"])
            or None,
            "REDIS_SESSION_PASSWORD": enable
            and self.get_value(env_vars, ["REDIS_SESSION_PASSWORD", "REDIS_PASSWORD"])
            or None,
        }


class CleverCloudCellarCompatibilityMapper(EnvMapper):
    """
    Compatibility mapper to convert Environment varaible provided by Cellar from CleverCloud
    https://www.clever-cloud.com/doc/deploy/addon/cellar/

    IS_TRUE(CELLAR_ADDON_HOST) => S3_FILESTORE_ENABLE
    CELLAR_ADDON_HOST => S3_FILESTORE_HOST
    CELLAR_ADDON_KEY_SECRET => S3_FILESTORE_SECRET_KEY
    CELLAR_ADDON_KEY_ID => S3_FILESTORE_ACCESS_KEY
    CELLAR_ADDON_REGION or "fr-par" => S3_FILESTORE_REGION
    """

    def map_vars(self, env_vars):
        # type: (Dict[str, Union[str, bool, int, None]]) -> Dict[str, Union[str, bool, int, None]]
        enable = self.is_true(
            env_vars.get(
                "S3_FILESTORE_ENABLE", bool(self.get_value(env_vars, ["S3_FILESTORE_HOST", "CELLAR_ADDON_HOST"]))
            )
        )
        return {
            "S3_FILESTORE_ENABLE": str(enable),
            "S3_FILESTORE_HOST": enable
            and self.get_value(env_vars, ["S3_FILESTORE_HOST", "CELLAR_ADDON_HOST"])
            or None,
            "S3_FILESTORE_SECRET_KEY": enable
            and self.get_value(env_vars, ["S3_FILESTORE_SECRET_KEY", "CELLAR_ADDON_KEY_SECRET"])
            or None,
            "S3_FILESTORE_ACCESS_KEY": enable
            and self.get_value(env_vars, ["S3_FILESTORE_ACCESS_KEY", "CELLAR_ADDON_KEY_ID"])
            or None,
            # Pas de region fournit par S3 CleverCloud
            "S3_FILESTORE_REGION": enable
            and self.get_value(env_vars, ["S3_FILESTORE_REGION", "CELLAR_ADDON_REGION"], default="fr-par")
            or None,
        }


class CleverCloudPostgresCompatibilityMapper(EnvMapper):
    def map_vars(self, env_vars):
        return {
            "DB_NAME": self.get_value(env_vars, ["DB_NAME", "DATABASE", "POSTGRESQL_ADDON_DB", "POSTGRES_DB"]),
            "DB_HOST": self.get_value(env_vars, ["DB_HOST", "POSTGRESQL_ADDON_DIRECT_HOST", "POSTGRESQL_ADDON_HOST"]),
            "DB_PORT": self.get_value(env_vars, ["DB_PORT", "POSTGRESQL_ADDON_DIRECT_PORT", "POSTGRESQL_ADDON_PORT"]),
            "DB_USER": self.get_value(env_vars, ["DB_USER", "POSTGRESQL_ADDON_USER", "POSTGRES_USER"]),
            "DB_PASSWORD": self.get_value(env_vars, ["DB_PASSWORD", "POSTGRESQL_ADDON_PASSWORD", "POSTGRES_PASSWORD"]),
        }
