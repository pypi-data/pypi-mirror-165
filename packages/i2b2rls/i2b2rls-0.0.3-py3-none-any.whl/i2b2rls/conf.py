from i2b2rls.utils import *
from copy import deepcopy
import yaml


@Singleton
class ConfigManager(GetData):
    """Parse and manage i2b2.yaml configuration"""

    def __init__(self, config_path=None):
        if config_path and os.path.isdir(config_path):
            self.path = os.path.abspath(config_path) + "/"
        else:
            self.path = os.getcwd() + "/"
        log.debug(f"Config path: {self.path}")
        self.yaml_file = self.path + "i2b2.yaml"
        self.sql_dir = self.path + "roles/"
        self.ds_dir = self.path + "datasources/"
        self.ds_template = self.path + "template-ds.xml"
        data = deepcopy(CONF_DEFAULTS)
        try:
            with open(self.yaml_file) as yf:
                data.update(yaml.full_load(yf))
                super().__init__(data)
        except Exception as err:
            raise Exception(f"Not an i2b2rls project folder ({err})")
        log.debug(f"Config path found: {self.path}")

        p = self.get("projects.default.pm")
        self.db_string = pg_db_string(
            p["admin-user"], p["admin-pass"], p["host"], p["port"], p["database"]
        )

    def get_project(self, project_id) -> GetData:
        defaults = deepcopy(CONF_DEFAULTS)
        base = defaults["projects"]["default"]
        user_defaults = self.get("projects.default")
        custom = self.get(f"projects.{project_id}")
        deep_update(base, user_defaults)
        deep_update(base, custom)

        project_data = {
            "project-path": base["project-path"] or f"/{project_id}",
            "nicename": base["nicename"] or project_id,
            "name": base["name"] or f"Project {project_id}",
            "description": base["description"] or f"i2b2 for {project_id}",
        }
        for cell_id in i2b2_CELL_MAP.keys():
            cell_config = base.get(cell_id, {})
            project_data[cell_id] = self.parse_cell_data(
                project_id, cell_id, cell_config
            )
        project_data = deep_update(base, project_data)
        members = project_data.get("members", {}) or {}
        parsed_members = {}
        for member, mdata in members.items():
            default_data = {
                "email": None,
                "password": None,
                "fullname": str(member).title(),
                "project-roles": project_data.get("default-project-roles"),
            }
            mdata = mdata or default_data
            if "ldap" in mdata:
                if not isinstance(mdata.get("ldap", None), dict):
                    mdata["ldap"] = project_data.get("ldap")
                else:
                    default_data["ldap"] = project_data["ldap"]
            parsed_members[member] = deep_update(deepcopy(default_data), mdata)
        project_data["members"] = parsed_members
        return GetData(project_data, name=project_id)

    @format_return()
    def parse_cell_data(self, project_id, cell_id, data, fmt=None):
        # Overwrite code-level defaults with user data
        data = deep_update(deepcopy(CELL_DEFAULTS), data)
        # Generate connection url for Datasources
        url = f"jdbc:postgresql://{data['host']}:{data['port']}/{data['database']}"
        # Generate pool-name for datasource if None
        pool = data["pool-name"] or f"{i2b2_CELL_MAP[cell_id]}{project_id}DS"
        # Generate jndi-name for datasource if None
        jndi = data["jndi-name"] or f"java:/{pool}"
        generated_data = {
            "connection-url": url,
            "jndi-name": jndi,
            "pool-name": pool,
            "db-datasource": jndi,
            "sql-path": os.path.join(self.sql_dir + data["sql-dir"]),
        }
        # Override empty user data with generated data
        deep_update(data, generated_data)
        data["db_string"] = pg_db_string(
            data["admin-user"],
            data["admin-pass"],
            data["host"],
            data["port"],
            data["database"],
        )
        return data

    @format_return("yaml")
    def add_project(self, project_id, save=False):
        project_data = {
            "project-path": f"/{project_id}/",
            "crc": {
                "ds-user": project_id + "_role",
                "ds-pass": project_id + "_pass",
                "provider-filter": project_id,
                "sql-dir": project_id + "_role",
            },
        }
        self.data["projects"][project_id] = project_data
        if save:
            safe_dump_yaml(data=self.data, file=self.yaml_file + ".bak")
        return project_data


i2b2_CELL_MAP = {
    "ont": "Ontology",
    "crc": "QueryTool",
    "work": "Workplace",
    "im": "IM",
    "pm": "i2b2pm",
}
i2b2_STATUS = {"A": "active", "D": "disabled"}
i2b2_LOOKUP_PATH = {"crc": "/{}/", "im": "{}/", "ont": "{}/", "work": "{}/"}
i2b2_SERVICE_ACCOUNT_ROLES = ["USER", "MANAGER", "DATA_OBFSC", "DATA_AGG"]
DS_NAMESPACE = "http://www.jboss.org/ironjacamar/schema"

LDAP_DEFAULTS = {
    "authentication-method": "LDAP",
    "connection-url": "ldap.example.com",
    "distinguished-name": "uid=",
    "search-base": "ou=people,dc=example,dc=org",
    "security-authentication": "simple",
}

PROJECT_DEFAULT_ROLES = [
    "USER",
    "DATA_DEID",
    "DATA_OBFSC",
    "DATA_AGG",
    "DATA_LDS",
    "EDITOR",
    "DATA_PROT",
]
CELL_DEFAULTS = {
    "host": "i2b2-pg",
    "port": 5432,
    "database": "i2b2",
    "jndi-name": None,
    "pool-name": None,
    "db-datasource": None,
    "connection-url": None,
    "admin-user": "i2b2",
    "admin-pass": "demouser",
    "ds-user": "i2b2",
    "ds-pass": "demouser",
    "schema": "public",
    "sql-dir": "template",
    "pg-vars": {"provider_filter": None},
    "server-type": "POSTGRESQL",
    "owner": "@",
    "driver": "postgresql-42.2.8.jar",
}

CONF_DEFAULTS = {
    "log-file": None,
    "service_user": "AGG_SERVICE_ACCOUNT",
    "log-level": "ERROR",
    "changeby-user": "i2b2rls",
    "wildfly-container": "i2b2-wildfly",
    "wildfly-datasources": "/opt/jboss/wildfly/standalone/deployments/",
    "projects": {
        "default": {
            "domain": "i2b2demo",
            "owner": "@",
            "project-path": None,
            "nicename": None,
            "name": None,
            "description": None,
            "members": {},
            "default-project-roles": PROJECT_DEFAULT_ROLES,
            "ldap": LDAP_DEFAULTS,
        },
    },
    "default-project-roles": PROJECT_DEFAULT_ROLES,
    "ldap": LDAP_DEFAULTS,
    "crc": CELL_DEFAULTS,
    "ont": CELL_DEFAULTS,
    "work": CELL_DEFAULTS,
    "im": CELL_DEFAULTS,
    "pm": CELL_DEFAULTS,
}
