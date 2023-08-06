#!/usr/bin/python3
# -*- coding: utf-8 -*-
from i2b2rls.conf import i2b2_LOOKUP_PATH, i2b2_SERVICE_ACCOUNT_ROLES
from i2b2rls.utils import *


class ProjectManager:
    """Manage and Deploy Projects configured in i2b2.yaml"""

    def __init__(self, conf, table, ds, role, user):
        self.ds = ds
        self.table = table
        self.conf = conf
        self.rls_role = role
        self.user = user
        self.project = None
        self.project_id = None

    def _init(self, project_id="default"):
        """Get full project tree from config object"""
        if project_id != self.project_id:
            log.info(f"Init project: {project_id}")
            try:
                self.project = self.conf.get_project(project_id)
                self.project_id = project_id
            except KeyError:
                raise Exception(f"Project not found: '{project_id}'")

    @format_return("yaml")
    def show(self, project_id, fmt=None) -> GetData:
        """Show the parsed config tree of given project"""
        return self.conf.get_project(project_id)

    @format_return()
    def list(self, fmt=None) -> dict:
        """Get list of projects and their status (registered/configured)"""
        projects = {}
        # Get projects from i2b2.yaml
        for p in self.conf.data["projects"]:
            projects[p] = {"configured": True, "registered": None}
        # Get projects from pm_project_data
        for p in self.list_registered(False):
            pname = p["project_id"]
            if pname in projects.keys():
                projects[pname]["registered"] = True
            else:
                projects[pname] = {"configured": False, "registered": True}
        return projects

    def list_registered(self, raise_on_err=True):
        try:
            return self.table.list("project")
        except Exception as err:
            if raise_on_err:
                raise err
            return {}

    #  ---- User Management -------------------------------------------------- #
    def add_pm_project_data(self, project_id, force=False):
        """Add project to i2b2pm.pm_project_data"""
        self._init(project_id)
        name = self.project.get("name")
        path = self.project.get("project-path")
        existing_project = self.table.get("project", project_id, n="all")
        if existing_project:
            log.warning(f"Project '{project_id}' exists!")
            return
        if force and existing_project:
            self.table.delete("project", project_id)
        self.table.add("project", project_id, name, None, None, path)
        log.info(f"Registered project '{project_id}'")

    @format_return()
    def get_cell_login(self, project_id, cell_id="crc", fmt=None) -> (str, str):
        """Return user + password from i2b2.yaml for the specified cell"""
        self._init(project_id)
        user = self.project.get(f"{cell_id}.ds-user")
        pw = self.project.get(f"{cell_id}.ds-pass")
        return user, pw

    @format_return()
    def get_members(self, project_id: str, fmt=None) -> dict:
        """Get a list of members in a project and their roles"""
        self._init(project_id)
        members = {}
        for role in self.table.list("project_role", project_id=project_id):
            u = role["user_id"]
            if u in members:
                members[u].append(role["user_role_cd"])
            else:
                members[u] = [role["user_role_cd"]]
        return members

    def register_members(self, project_id, skip_error=False):
        """Register project members with default roles"""
        self._init(project_id)
        members = self.project["members"]
        for user_id, data in members.items():
            roles = data.get("roles", self.project["default-project-roles"])
            log.info(f"Adding user '{user_id}': {roles}")
            self.user.add(user_id, data["password"], data["fullname"], data["email"])
            self.user.add_roles(project_id, user_id, roles)
            if data.get("ldap", None):
                log.info(f"Adding LDAP for user '{user_id}'")
                self.set_user_ldap(project_id, user_id, data["ldap"])

    def unregister_members(
        self, project_id, members=None, del_roles=True, del_users=True
    ):
        """Delete members and/or roles from i2b2 project management cell"""
        self._init(project_id)
        members = members or self.project["members"].keys()
        for user_id in members:
            log.debug(f"Unregistering member {user_id} (Delete: {del_users})")
            self.user.delete(user_id) if del_users else None
            self.del_user_ldap(project_id, user_id) if del_users else None
            self.user.del_roles(project_id, user_id) if del_roles else None

    def add_service_roles(self, project_id):
        """ Set project roles for user 'AGG_SERVICE_ACCOUNT'"""
        self.user.add_roles(
            project_id, "AGG_SERVICE_ACCOUNT", i2b2_SERVICE_ACCOUNT_ROLES
        )

    def set_user_ldap(self, project_id, user_id, data=None):
        """Get LDAP settings from i2b2.yaml and set for give user"""
        self._init(project_id)
        project_ldap = self.project.get("ldap")
        user_ldap = self.project.get(f"members.{user_id}.ldap", {})
        project_ldap.update(user_ldap)
        if type(data) == dict and len(data) > 0:
            project_ldap.update(data)
        for k, v in project_ldap.items():
            log.debug(f"Add {k}:{v} to user '{user_id}'")
            if len(self.table.get("user_param", user_id, k, n="all")) > 0:
                self.table.update("user_param", user_id, k, "value", v)
            else:
                self.table.add("user_param", user_id, k, v, "T")

    def del_user_ldap(self, project_id, user_id):
        self._init(project_id)
        project_ldap = self.project.get("ldap")
        user_ldap = self.project.get(f"members.{user_id}.ldap", {})
        project_ldap.update(user_ldap)
        for k, v in project_ldap.items():
            log.debug(f"Delete {k}:{v} from user '{user_id}'")
            self.table.delete("user_param", user_id, k)

    #  ---- Datasource stuff ------------------------------------------------- #
    @try_exit
    def add_db_lookup(self, project_id: str, cell_id: str):
        """Create row in i2b2hive.cell_db_lookup for cell"""
        self._init(project_id)
        lookup_map = {
            "c_domain_id": self.project["domain"],
            "c_project_path": i2b2_LOOKUP_PATH[cell_id].format(project_id),
            "c_owner_id": self.project["owner"],
            "c_db_fullschema": self.project[cell_id]["schema"],
            "c_db_datasource": self.project[cell_id]["jndi-name"],
            "c_db_servertype": "POSTGRESQL",
            "c_db_nicename": self.project["nicename"],
        }
        self.table._init_table(f"{cell_id}_db_lookup")
        t = self.table.sa_table(**lookup_map)
        self.table.db.add(t)
        log.info(f"Added DS {lookup_map['c_db_datasource']}")

    @try_exit
    def delete_db_lookup(self, project_id, cell_id):
        """Delete db_lookup for for given cell"""
        self._init(project_id)
        filters = {
            "c_domain_id": self.project["domain"],
            "c_project_path": i2b2_LOOKUP_PATH[cell_id].format(project_id),
            "c_owner_id": self.project["owner"],
        }
        results = self.table.query_dict(f"{cell_id}_db_lookup", filters).all()
        for r in results:
            self.table.db.delete(r)

    def create_db_lookups(self, project_id):
        """Conveniently register all db_lookups for crc, im, ont & work"""
        for cell_id in ["im", "crc", "work", "ont"]:
            self.add_db_lookup(project_id, cell_id)

    def delete_db_lookups(self, project_id):
        """Conveniently delete all db_lookups for crc, im, ont & work"""
        for cell_id in ["im", "crc", "work", "ont"]:
            self.delete_db_lookup(project_id, cell_id)

    def generate_ds(
        self,
        project_id: str,
        cell_id: str = "crc",
        overwrite: bool = True,
        stdout: bool = False,
        deploy: bool = True,
        extract: bool = True,
    ):
        """Create Datasource for given cell
        Args:
            project_id: Name of project defined in i2b2.yaml
            cell_id: Name of cell to deploy [crc|im|ont|work]
            overwrite: Remove existing Datasource if already exists
            stdout: Print generated Datasource
            deploy: Copy ds-files to wildfly server and reload
            extract: Copy ds-files from wildfly server before running
        """
        self._init(project_id)
        self.ds.extract() if extract else None
        if overwrite:
            pool = self.project.get(f"{cell_id}.pool-name")
            self.ds.delete(pool)
        ds_data = self.project.get(f"{cell_id}")
        ds = self.ds.add(f"rls-ds.xml", ds_data)
        self.ds.deploy() if deploy else None
        print(self.ds) if stdout else None
        log.info(f"Generated DS for '{project_id}': {cell_id}")

    @try_exit
    def delete_ds(self, project_id, cell_id="crc", deploy=True):
        """Remove Datasource for given cell"""
        self._init(project_id)
        self.ds.extract()
        pool = self.project.get(f"{cell_id}.pool-name")
        self.ds.delete(pool)
        if deploy:
            self.ds.deploy()

    def generate_sql(self, project_id: str, cell_id: str = "crc", force: bool = False):
        """
        Copy template SQL folder to the project's datasource
        Args:
            project_id: Name of project defined in i2b2.yaml
            cell_id: Name of cell to deploy [crc|im|ont|work]
            force: Remove folder if it already exists
        """
        self._init(project_id)
        sql_path = self.project.get(cell_id)["sql-path"]
        template_path = self.conf.sql_dir + "template"
        if sql_path == template_path:
            log.warning("sql-path is template path, skipping...")
            return
        try:
            copy_folder(template_path, sql_path, overwrite=force)
        except FileExistsError as err:
            log.warning(f"{repr(err)} Use --force=True to overwrite")

    def run_rls(
        self,
        project_id: str,
        cell_id: str = "crc",
        generate: bool = True,
        script: str = "main.sql",
        skip_error: bool = False,
    ):
        """Run SQL file from the projects datasource user
        Args:
            project_id: ID of project as in i2b2.yaml
            cell_id: The cell data to deploy
            generate: Copy template folder to new dir named after the rls user
            script: Specify .sql file from the role folder
            skip_error: Do not raise Exceptions if True
        """
        self._init(project_id)
        cell = self.project.get(cell_id)
        user, pw = self.get_cell_login(project_id, cell_id)
        role_dir = cell["sql-dir"]
        if not os.path.isdir(role_dir) and generate:
            self.generate_sql(project_id, cell_id, False)

        log.debug(f"Role dir is {role_dir}")
        data = {
            "project_id": project_id,
            "role_name": user,
            "role_pass": pw,
            "db": cell["database"],
            "cell_schema": cell["schema"],
        }
        data.update(cell["pg-vars"])
        providers = data["provider_filter"]
        if type(providers) == list:
            data["provider_filter"] = ",".join([p for p in providers])
        try:
            self.rls_role.apply(role_dir, cell["db_string"], script, data=data)
        except Exception as err:
            log.error(err)
            if not skip_error:
                raise err
        log.info(f"Ran rls for {project_id}")

    def register(
        self,
        project_id: str,
        cell_id: str = "crc",
        force: bool = False,
        ignore_errors: bool = False,
        add_i2b2: bool = False,
        deploy_ds: bool = True,
        extract_ds: bool = True,
    ):
        """Create all resources for a RLS project

        Steps:
        * (Optional) Create SQL script from template
        * Run SQL files in role folder
        * Create & deploy Datasource file for CRC cell
        * Create the project in i2b2pm.pm_project_data
        * Create mandatory i2b2-roles for AGG_SERVICE_ACCOUNT
        * Register project db_lookups in i2b2hive.{im,ont,work,crc}_db_lookup

        Args:
            project_id: ID of project as in i2b2.yaml
            cell_id: The cell data to deploy (Default: 'crc')
            init: Create sql-script from template if none exists
            force: Delete Existing resources and recreate them
            ignore_errors: Ignore errors and continue creating resources
            add_i2b2: Add 'i2b2' user to project with default roles
            deploy_ds: Copy Datasource file to wildfly server and reload
            extract_ds: Pull Datasource file from wildfly server to local folder
        """
        self._init(project_id)
        self.table.db.autocommit = ignore_errors
        # Run SQL
        self.run_rls(project_id, cell_id, generate=True)
        # Deploy crc-ds.xml
        self.generate_ds(project_id, cell_id, deploy=deploy_ds, extract=extract_ds)
        # Add project to pm_project_data
        self.add_pm_project_data(project_id, force=force)
        if add_i2b2:
            self.user.add_roles(
                project_id, "i2b2", self.project["default-project-roles"]
            )
        # Add users to pm_user_data
        self.register_members(project_id)
        # Add roles to pm_project_user_roles
        self.add_service_roles(project_id)
        # Add datasource to crc_db_lookup
        self.create_db_lookups(project_id)
        log.info(f"Registered project '{project_id}'")

    def register_all(self, force=False):
        """Register all project from 'i2b2.yaml'"""
        self.ds.extract()
        for p in [k for k in self.conf.get("projects") if k != "default"]:
            self.register(
                p, deploy_ds=False, extract_ds=False, force=force, ignore_errors=force
            )
            self.show(p, fmt="yaml")
        self.ds.deploy()

    def unregister(self, project_id, cell_id="crc", del_users=False):
        """Unregister project resources from datasources, pm and database"""
        self.run_rls(project_id, cell_id, script="drop.sql", skip_error=True)
        self.delete_db_lookups(project_id)
        self.delete_ds(project_id, cell_id=cell_id)
        self.table.delete("project", project_id)
        if del_users:
            self.unregister_members(project_id, del_users=del_users, del_roles=1)
            self.unregister_members(project_id, ["i2b2", "AGG_SERVICE_ACCOUNT"])
        log.info(f"Unregistered project '{project_id}'")

    def unregister_all(self, force=False):
        """Register all project from 'i2b2.yaml'"""
        for p in [k for k in self.conf.get("projects") if k != "default"]:
            self._init(p)
            self.unregister(p, del_users=force)
