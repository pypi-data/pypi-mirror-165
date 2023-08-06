#!/usr/bin/python3
# -*- coding: utf-8 -*-
from automapdb import TableManager
from automapdb.db import AutoMapDB
from i2b2rls.datasource import DatasourceManager
from i2b2rls.project import *
from i2b2rls.role import RoleManager
from i2b2rls.user import UserManager
from i2b2rls.conf import ConfigManager, i2b2_STATUS
from i2b2rls.cli import CLI
import i2b2rls.utils
import os
import fire


class i2b2fire:
    """Command Line Interface for i2b2rls

    i2b2fire is called from the fire cli and python code alike, giving both
    central access to submodules and conf_path.
    The constructor arguments are used as cli parameters to configure
    the basic behaviour of the application.

    Args:
      log_level: Set logging level [debug|info|warning|error|critical]
      verbose: Add verbosity - overrides log_level with 'DEBUG'
      config: Path to i2b2rls config folder with i2b2.yaml
      init: Initiate project folder, use with --conf / -c
      autocommit: Make database api commit after every statement
    """

    def __init__(
        self,
        autocommit: bool = False,
        conf: os.PathLike = None,
        log_level: str = None,
        verbose: bool = False,
        init: bool = False,
    ):
        # Setup runtime and config path
        self.run_dir = os.path.dirname(os.path.abspath(__file__))
        config_path = os.getenv("I2B2RLS_CONF", conf)
        if config_path and init:
            self.init(config_path)
        self.conf = ConfigManager(config_path)

        # Configure logger
        lvl = "debug" if verbose else log_level or self.conf.get("log-level")
        log = set_logger(lvl)
        log.debug(f"Running in {self.run_dir}")

        # Create subcommand groups
        self.ds = DatasourceManager(self.conf)
        self.db = AutoMapDB(self.conf.db_string, autocommit=autocommit)
        self.table = TableManager(
            self.db, self.run_dir + "/tables.json", default_values=i2b2_column_defaults
        )
        self.user = UserManager(self.table)
        self.role = RoleManager(self.conf)
        self.cmd = CLI(self)
        self.project = ProjectManager(
            self.conf, self.table, self.ds, self.role, self.user
        )
        self.utils = i2b2rls.utils

    def status(self, table, *args):
        """Get the status of an i2b2 table object (user, project etc.) """
        try:
            data = self.table.get(table, *args)
            status = i2b2_STATUS[data["status_cd"]]
            return True, f"{table.title()} exists and is {status}"
        except Exception as err:
            return False, f"{table.title()} not found. ({err})"

    @staticmethod
    def init(path="."):
        """Initiate project folder with i2b2.yaml, datasources and sql files"""
        run_dir = os.path.dirname(os.path.abspath(__file__))
        template_source = run_dir + "/config.default"
        target_parent_dir = os.path.abspath(path)
        target = os.path.abspath(target_parent_dir)
        if os.path.isdir(template_source):
            if not os.path.isdir(target):
                os.mkdir(target)
            cmd = f"cp -rv {template_source}/* {target}"
            vrun(cmd)
        return target


def main():
    try:
        fire.Fire(i2b2fire)
    except Exception as err:
        log.error(err)
        raise err


if __name__ == "__main__":
    main()
