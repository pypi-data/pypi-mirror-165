#!/usr/bin/python3
# -*- coding: utf-8 -*-
from i2b2rls.utils import *


class RoleManager:
    """Manage and run SQL scripts for Postgres Roles"""

    def __init__(self, conf):
        self.conf = conf

    @format_return()
    def list(self, fmt="") -> dict:
        roles = {}
        for role_dir in os.scandir(self.conf.sql_dir):
            if role_dir.is_dir():
                roles[str(role_dir.name)] = {
                    "path": role_dir.path,
                    "files": find_files(role_dir.path, ".sql"),
                }
        return roles

    @format_return()
    def get(self, role_name, fmt=None):
        try:
            return self.list()[role_name]
        except KeyError as err:
            raise KeyError(f"SQL folder '{role_name}' not found")

    def apply(self, role_name, db_string, script="main.sql", data=None):
        """Apply .sql files found in a role folder"""
        role = self.get(role_name)
        try:
            sqlfile = [f for f in role["files"] if f.name == script][0]
        except IndexError as err:
            raise FileNotFoundError(f'{role["path"]}/{script}')
        out, err, ret = psql(db_string, sqlfile.path, data=data)
        for line in out.split("\n") + err.split("\n"):
            if "ERROR" in line:
                raise SQLException(line)
            else:
                log.debug(line)
