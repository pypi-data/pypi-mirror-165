#!/usr/bin/python3
# -*- coding: utf-8 -*-

from i2b2rls.utils import *
from i2b2rls.conf import ConfigManager
from xml.dom.minidom import parse, Element, Document, Node, parseString
from dataclasses import dataclass
from i2b2rls.conf import DS_NAMESPACE


@dataclass
class Datasource:
    """Holds basic details about a datasource scanned by `Datasources`."""

    path: str
    dom_index: int
    doc: Document
    ds: Element
    name: str = None

    def __post_init__(self):
        self.name = self.ds.getAttribute("pool-name")
        self.filename = self.path.split("/")[-1]

    def __repr__(self) -> str:
        return self.ds.toxml()


class DatasourceManager:
    """Edit Wildfly Datasources"""

    def __init__(self, conf: ConfigManager):
        """Manipulate wildfly datasource files.

        ## Datasources
        Datasources are used to handle database connections from wildfly.
        This module can edit datasources and files,
        and deploy them to the server.
        Datasources are identified by their pool name, e.g. WorkplaceBootStrapDS.

        ## Usage
        To work on the datasource files, use `extract` to copy the xml files
        from the server to your dev folder. Then you can use
        `list, add, delete` to manipulate them.
        Use `deploy` to copy the files back to the deployment folder
        and optionally reload the wildfly daemon for a config change.

        ## Hierarchy
        ~~~xml
        datasources/  # Folder containing development XML files
        |- rls-ds.xml  # wildfly deployment file, contains multiple datasources
        |--- <datasources>  # root xml tree -> _Document_ object
        |----- <datasource pool-name="">  # Datasource, identified by pool name
        ~~~
        """
        self.ds_files = None
        self.conf = conf
        self.dev_dir = self.conf.ds_dir
        self.prod_dir = self.conf.get("wildfly-datasources")
        self.container = self.conf.get("wildfly-container")
        self.load_datasources()

    def load_datasources(self):
        self.ds_files = {}
        # List all the xml files in the ds_dev_dir
        xml_files = [f for f in os.listdir(self.dev_dir) if f.endswith(".xml")]
        for file_name in xml_files:
            file_path = self.dev_dir + file_name
            # Parse xml tree to Document object
            doc = parse(file_path)
            self.ds_files[file_path] = []
            log.debug(f"DS file: {file_name}")
            # Loop through all the datasources in the Document
            for i, ds_elem in enumerate(doc.getElementsByTagName("datasource")):
                # Create Datasource object with node_index
                ds = Datasource(file_path, dom_index=i, doc=doc, ds=ds_elem)
                self.ds_files[file_path] += [ds]
                log.debug(f"DS entry: {ds.name}")

    @format_return()
    def list(self, fmt=0) -> dict:
        """Searches datasource files for a pool """
        return {f: [x.name for x in d] for f, d in self.ds_files.items()}

    def get(self, pool_name, fmt=0) -> Datasource or None:
        """Searches datasource files for a pool """
        for path, datasources in self.ds_files.items():
            for ds in datasources:
                if ds.name == pool_name:
                    log.info(f"Found Datasource: {ds.name}, {ds.path}")
                    return ds
        log.warning(f"Datasource not found: {pool_name}")
        return None

    def delete(self, pool_name: str, delete_file: bool = False) -> str:
        """Deletes datasource from pool and file if delete_file is True"""
        ds = self.get(pool_name)
        if ds is None:
            return
        log.debug(f"Datasource: {pool_name} {ds.path}")
        ds.doc.documentElement.removeChild(ds.ds)
        if delete_file:
            if len(ds.doc.getElementsByTagName("datasource")) == 0:
                log.warning(f"Removing {ds.path}")
                os.remove(ds.path)
        xml_file_dump(ds.path, ds.doc)
        self.load_datasources()

    def add(self, ds_file="rls-ds.xml", ds_data=None, save=True):
        """Create new datasource Tree and append it to file

        If the file exists, the new datasource is inserted.
        Args:
            ds_file (str): Filename of Datasource
            ds_data (dict): dict with datasouce data.
        """
        ds = self.get(ds_data.get("pool-name"))
        if ds is not None:
            return f"Pool exists: {ds.name}: {ds.path}"
        with open(self.conf.ds_template) as file:
            template = "".join(file.readlines()).format(**ds_data)
        file_path = self.dev_dir + ds_file
        try:
            doc = self.ds_files[file_path][0].doc
        except Exception as err:
            log.warning(repr(err))
            doc = xml_set_namespace(Document(), DS_NAMESPACE)
        ds_tree = parseString(template).childNodes[0]
        doc.childNodes[0].appendChild(ds_tree)
        self.load_datasources()
        if save:
            xml_file_dump(file_path, doc)
        return prettyxml(doc)

    def extract(self, file="rls-ds.xml"):
        """Creates local dev files from production datasources

        Copies wildfly's datasource files from the production dir
        to the dev dir using `docker cp`.
        This requires a temporary folder inside the container
        as `docker cp` can only copy whole directories.
        """
        cp = f"docker cp {self.container}:{self.prod_dir+file} {self.conf.ds_dir}"
        try:
            vrun(cp)
        except Exception as err:
            print(err)
            return
        log.info(f"Extracted file: {os.listdir(self.conf.ds_dir)}")

    def deploy(self, file=None, reload=True):
        """Move dev files to wildlfy production dir, verify and reload"""
        ds_files = [file] if file else self.ds_files.keys()
        for ds_file in ds_files:
            cmd = f"docker cp {ds_file} {self.container}:{self.prod_dir}"
            log.debug(f"{cmd}")
            vrun(cmd)
        docker_exec(self.container, f"ls -l {self.prod_dir}*.xml.*")
        self.reload() if reload else None

    def log_on(self):
        cmd = "sed -i 's/INFO/DEBUG/g' /opt/jboss/wildfly/standalone/configuration/standalone.xml"
        docker_exec(self.container, cmd, opts="-u root")

    def reload(self):
        log.info(f"Reloading wildfly ({self.container})...")
        docker_exec(self.container, "/opt/jboss/wildfly/bin/jboss-cli.sh -c " "reload")
