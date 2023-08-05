# -*- coding: utf8 -*-
import logging
import os
import time

import odoo
from checksumdir import dirhash

__version__ = odoo.release.version

_logger = logging.getLogger("ndpserver")
handler = logging.StreamHandler()
_logger.addHandler(handler)
_logger.setLevel(logging.DEBUG)

old_create_empty_database = odoo.service.db._create_empty_database
old_modules_loading_load_modules = odoo.modules.loading.load_modules


def _patch_create_empty_database(name):
    if odoo.service.db.exp_db_exist(name):
        raise odoo.service.db.DatabaseExists("database %r already exists!" % (name,))
    return old_create_empty_database(name)


old_odoo_service_db_list_dbs = odoo.service.db.list_dbs


def _patch_list_dbs(force=False):
    if not odoo.tools.config["list_db"] and not force:
        raise odoo.exceptions.AccessDenied()
    if odoo.tools.config["db_name"]:
        return [odoo.tools.config["db_name"]]
    return old_odoo_service_db_list_dbs(force)


_old_odoo_sql_db_db_connect = odoo.sql_db.db_connect

old_odoo_cli_server_report_configuration = odoo.cli.server.report_configuration


def _report_configuration():
    """Log the server version and some configuration values.

    This function assumes the configuration has been initialized.
    """
    config = odoo.tools.config
    odoo.cli.server._logger.info("Odoo version %s", __version__)
    if os.path.isfile(config.rcfile):
        odoo.cli.server._logger.info("Using configuration file at " + config.rcfile)
    odoo.cli.server._logger.info("addons paths:")
    odoo.cli.server._logger.info("\n".join(odoo.modules.module.ad_paths))
    host = config["db_host"] or os.environ.get("PGHOST", "default")
    port = config["db_port"] or os.environ.get("PGPORT", "default")
    user = config["db_user"] or os.environ.get("PGUSER", "default")
    odoo.cli.server._logger.info("database: %s@%s:%s", user, host, port)
    odoo.cli.server._logger.info("database: max conn %s", config["db_maxconn"])
    odoo.cli.server._logger.info("Loaded module: %s", config["server_wide_modules"])
    odoo.cli.server._logger.info("Stop after init: %s", config["stop_after_init"])


def _patch_db_connect(to, allow_uri=False):
    db_name = odoo.tools.config["db_name"]
    if odoo.tools.config["db_name"] != to:
        _logger.info("Try Connect to [%s] DB connect to [%s] DB instead", to, db_name)
        to = db_name
    return _old_odoo_sql_db_db_connect(to, allow_uri=allow_uri)


CREATE_CHECKSUM_TABLE = """
CREATE TABLE IF NOT EXISTS addons_path_checksum (
    path     character varying NOT NULL,
    checksum character varying NOT NULL,
    primary key (checksum, path)
)"""


def _path_modules_loading_load_modules(db, force_demo=False, status=None, update_module=False):
    if not update_module or odoo.tools.config["init"]:
        return old_modules_loading_load_modules(db, force_demo, status, update_module)

    with db.cursor() as cr:
        cr.execute(CREATE_CHECKSUM_TABLE)
        cr.execute("SELECT path, checksum from addons_path_checksum")
        data = cr.fetchall()

    values = {}
    for ad_path in odoo.tools.config["addons_path"].split(","):
        ts = time.time()
        values[ad_path] = dirhash(
            ad_path,
            "sha256",
            ignore_hidden=True,
            excluded_extensions=[
                "pyc",
            ],
        )
        _logger.info("Hashing %s in %ss => %s", ad_path, round(time.time() - ts, 2), values[ad_path])
    for path, cheksum in data:
        if values.get(path) != cheksum:
            break
    else:
        update_module = {}
        odoo.tools.config["update"] = {}

    result = old_modules_loading_load_modules(db, force_demo, status, update_module)
    with db.cursor() as cr:
        cr.execute("""TRUNCATE addons_path_checksum RESTART IDENTITY""")
        for path, checksum in values.items():
            cr.execute("""INSERT INTO addons_path_checksum (path, checksum) VALUES (%s, %s)""", (path, checksum))
        cr.commit()

    return result


def _applier(src, new):
    _logger.info("> apply patch %s#%s on > %s#%s", new.__module__, new.__name__, src.__module__, src.__name__)
    if os.environ.get("REMOTE_DB", str(True)) == "False":
        return src
    return new


def apply_hard_monkey_patch():
    _logger.info(">>>>>>>>>>>>> PATCHING ODOO >>>>>>>>>>>>>")
    odoo.sql_db.db_connect = _applier(odoo.sql_db.db_connect, _patch_db_connect)
    odoo.service.db._create_empty_database = _applier(
        odoo.service.db._create_empty_database, _patch_create_empty_database
    )
    odoo.cli.server.report_configuration = _applier(odoo.cli.server.report_configuration, _report_configuration)
    odoo.modules.loading.load_modules = _applier(odoo.modules.loading.load_modules, _path_modules_loading_load_modules)
    odoo.modules.load_modules = _applier(odoo.modules.load_modules, _path_modules_loading_load_modules)
    _logger.info("<<<<<<<<<<<<< PATCHING ODOO <<<<<<<<<<<<<")
