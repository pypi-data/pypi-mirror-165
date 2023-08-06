#!/usr/bin/python3
# -*- coding: utf-8 -*-
from i2b2rls.utils import *


class UserManager:
    """Manage Users & Roles in i2b2 database"""

    def __init__(self, table):
        self.table = table

    def add(self, user_id, password=None, fullname=None, email=None, force=False):
        """Create user in i2b2pm.pm_user_roles"""
        if self.get(user_id, n="all", fmt=None):
            if force:
                self.delete(user_id)
            else:
                log.warning(f"User '{user_id}' exists, skipping!")
                return False
        fullname = fullname if fullname else user_id.title()
        password = i2b2_password_cryptor(password) if password else None
        email = email if email else None
        self.table.add("user", user_id, fullname, password, email)
        log.info(f"Added user: {user_id}")

    @format_return("yaml")
    def get(self, user_id, n="one", fmt=None):
        """Query user from pm_user_data"""
        return self.table.get("user", user_id, n=n)

    @format_return("yaml")
    def list(self, fmt=None):
        """Query user from pm_user_data"""
        return self.table.list("user")

    def delete(self, user_id):
        """Delete user from i2b2 backend pm_user_data"""
        return self.table.delete("user", user_id)

    @format_return()
    def get_roles(self, project_id, user_id, fmt=None):
        """Show all roles a user has in pm_project_user_oles"""
        roles = self.table.get(
            "project_role", project_id, user_id, fields="user_role_cd", n="all"
        )
        return [r["user_role_cd"] for r in roles]

    def add_roles(self, project_id, user_id, roles=None):
        """Add user to i2b2pm.pm_project_user_roles with default roles"""
        existing_roles = self.get_roles(project_id, user_id)
        for role in roles:
            if role in existing_roles:
                log.warning(f"User '{user_id}' has role: '{role}'")
            else:
                self.table.add("project_role", project_id, user_id, role)
                log.info(f"Added role {project_id}: {role} to user {user_id}")

    def del_roles(self, project_id, user_id):
        """Delete all roles a user has in pm_project_user_roles"""
        for role in self.get_roles(project_id, user_id):
            self.table.delete("project_role", project_id, user_id, role)
            log.info(f"Deleted role {project_id}: {role} from user {user_id}")
