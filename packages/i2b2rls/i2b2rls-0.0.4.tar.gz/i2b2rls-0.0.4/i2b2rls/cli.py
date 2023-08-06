#!/usr/bin/python3
# -*- coding: utf-8 -*-

import logging
from i2b2rls.utils import sys_exit, fmt_data, joinsep


class CLI:
    def __init__(self, i2b2fire):
        self.user = UserCLI(i2b2fire)
        self.group = ProjectCLI(i2b2fire)


class UserCLI:
    def __init__(self, _i2b2fire):
        self.i2b2fire = _i2b2fire

    @sys_exit()
    def add(self, user_id, password=None, fullname=None, email=None):
        return self.i2b2fire.user.add(user_id, password, fullname, email)

    @sys_exit()
    def delete(self, user_id):
        return self.i2b2fire.user.delete(user_id)

    @sys_exit()
    def set_ldap(self, user_id, project_id="default"):
        self.i2b2fire.project.set_user_ldap(project_id, user_id)
        return True

    @sys_exit()
    def status(self, user_id: str):
        return self.i2b2fire.status("user", user_id)[0]

    @sys_exit()
    def lock(self, user_id):
        self.i2b2fire.table.update("user", user_id, "status_cd", "D")
        return True

    @sys_exit()
    def is_locked(self, user_id):
        res = self.i2b2fire.status("user", user_id)[1]
        return True if "disabled" in res else False

    @sys_exit()
    def unlock(self, user_id):
        self.i2b2fire.table.update("user", user_id, "status_cd", "A")
        return True

    @sys_exit(none_on_success=False)
    def show(self, user_id, fmt="yaml"):
        return fmt_data(self.i2b2fire.table.get("user", user_id), fmt)

    @sys_exit(none_on_success=False)
    def list(self, fmt="json", fields: list = None):
        return self.i2b2fire.table.list("user", fields=["user_id"], fmt=fmt)


class ProjectCLI:
    def __init__(self, _i2b2fire):
        self.i2b2fire = _i2b2fire

    @sys_exit()
    def add_user(self, user_id: str, project_id: str, roles: list = None):
        self.i2b2fire.project._init(project_id)
        roles = roles or self.i2b2fire.project.project["default-project-roles"]
        self.i2b2fire.user.add_roles(project_id, user_id, roles)

    @sys_exit()
    def remove_user(self, user_id: str, project_id: str, delete_user: bool = False):
        self.i2b2fire.project.unregister_members(
            project_id, members=[user_id], del_users=delete_user
        )

    @sys_exit()
    def register(self, project_id: str, cell: str = "crc"):
        self.i2b2fire.project.register(project_id, cell)

    @sys_exit()
    def unregister(self, project_id, cell_id: str = "crc", del_members: bool = False):
        self.i2b2fire.project.unregister(project_id, cell_id, del_users=del_members)

    @sys_exit()
    def exists(self, project_id):
        return self.i2b2fire.status("project", project_id)

    @sys_exit(none_on_success=False)
    def get_members(self, project_id):
        data = self.i2b2fire.project.get_members(project_id)
        return joinsep(data.keys(), sep=" ").replace("'", "")

    @sys_exit(none_on_success=False)
    def list(self):
        return self.i2b2fire.project.list()
