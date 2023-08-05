# -*- coding: utf8 -*-
import logging
import os

import odoo
from maintenance_server import run_from_env

from . import cloud_monkey_patch

_logger = logging.getLogger("ndpserver")


class NdpServer(odoo.cli.Command):
    """
    Command ndpserver au lieu d'utliser le server classique fournit par Odoo

    Ce serveur ajoute des monkey patch pour empecher Odoo de decouvrir les base de donnée si `db_name` est fournit
    Construit le fichier de configuration à la volé en fonction des variable d'environement

    Puis lance la cmd classique d'Odoo
    """

    def run(self, args):
        cloud_monkey_patch.apply_hard_monkey_patch()
        odoo.cli.server.main(args)


class ServerMaintenance(odoo.cli.Command):
    def run(self, args):
        html_file_path = os.environ.get("MAINTENANCE_PAGE")
        os.environ["MAINTENANCE_PAGE"] = html_file_path or os.path.join(
            os.path.dirname(__file__), "..", "static", "html", "maintenance.html"
        )
        return run_from_env()


class ConfigCreate(odoo.cli.Command):
    """
    This module is only here to create a config odoo and stop right after
    You don't need to add `--stop-after-init` in args.

    This is useful if you wnat to create a config file to test it
    or if you don't want to change your args with or without `-u my_module`
    This launcher don't care of `-u` or `-i`
    """

    def run(self, args):
        odoo.tools.config.parse_config(args)
        odoo.tools.config.save()
