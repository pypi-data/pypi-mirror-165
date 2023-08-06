#!/usr/bin/python3
# -*- coding: utf-8 -*-
from subprocess import Popen, PIPE
from collections.abc import Mapping
import shutil
import os, sys, json, yaml
from xml.dom import minidom
import logging
import inspect
from pprint import pformat
import hashlib
import functools
from typing import *

log = logging.getLogger(__name__)


FONT_MODS = {
    "HEADER": "\033[95m",
    "OKBLUE": "\033[94m",
    "INFO": "\033[94m",
    "OKGREEN": "\033[92m",
    "WARNING": "\033[93m",
    "WARN": "\033[93m",
    "ERROR": "\033[91m",
    "ENDC": "\033[0m",
    "B": "\033[1m",
    "UL": "\033[4m",
}

# logging
LOG_LEVEL_MAP = {
    "CRITICAL": logging.CRITICAL,
    "ERROR": logging.ERROR,
    "WARN": logging.WARNING,
    "WARNING": logging.WARNING,
    "INFO": logging.INFO,
    "DEBUG": logging.DEBUG,
}

i2b2_column_defaults = {
    "change_date": "NOW()",
    "entry_date": "NOW()",
    "c_change_date": "NOW()",
    "c_entry_date": "NOW()",
    "status_cd": "A",
    "c_status_cd": "A",
    "changeby_char": "i2b2rls",
}


def set_logger(lvl: str = "info", log_file: str = "/tmp/i2b2.log"):
    lvl = lvl.upper()
    sys.tracebacklimit = None if lvl == "DEBUG" else 0
    sh = logging.StreamHandler(sys.stdout)
    # sh.setFormatter(CustomFormatter())
    handlers = [sh]
    if log_file and os.path.isdir(os.path.dirname(log_file)):
        handlers += [logging.FileHandler(log_file)]
    logging.basicConfig(
        format="%(asctime)s | %(levelname)-8s | %(funcName)-15s | %(message)s",
        handlers=handlers,
        level=LOG_LEVEL_MAP[lvl],
        datefmt="%H:%M:%S",
    )
    log.debug(f"Log level: {lvl}")
    log.debug(f"Traceback: {sys.tracebacklimit}")
    return log


def sys_exit(on_false=True, on_error=True, exit_code=1, none_on_success=True):
    """Raise sys.exit after functions that are used as cli commands"""

    def exit_err_decorator(func):
        @functools.wraps(func)
        def wrapper(self="None", *args, **kwargs):
            cls_name = self.__class__.__name__
            log.debug(f"[try ] {func.__name__}, {cls_name}, {args}, {kwargs}")
            try:
                data = func(self, *args, **kwargs)
                if data is False and on_false:
                    sys.exit(exit_code)
                if none_on_success:
                    return None
                return data
            except Exception as err:
                log.error(f"{func.__name__}: {err}")
                if on_error:
                    sys.exit(exit_code)

        return wrapper

    return exit_err_decorator


def try_exit(func):
    @functools.wraps(func)  # Preserves function attributes, e.g. __doc__
    def wrapper(self, *args, **kwargs):
        cls_name = self.__class__.__name__
        log.debug(f"[try ] {func.__name__}, {cls_name}, {args}, {kwargs}")
        ignore_errors = kwargs.pop("ignore_errors", False)
        try:
            return func(self, *args, **kwargs)
        except Exception as err:
            log.warning(f"{func.__name__}: {err}")
            if not ignore_errors:
                raise err

    return wrapper


# FORMATTING AND DATA STRUCTURES
# -------------------------------
def deep_update(source, overrides):
    for key, value in overrides.items():
        if isinstance(value, Mapping) and value:
            returned = deep_update(source.get(key, {}), value)
            source[key] = returned
        else:
            source[key] = overrides[key]
    return source


def merge_dict(a, b):
    a_temp = a.copy()
    for k, v in b.items():
        if k not in a_temp:
            a[k] = v


def colorize(data, lvl="ERROR", ul=False, b=True) -> str:
    mods = FONT_MODS[lvl]
    mods += FONT_MODS["UL"] if ul else ""
    mods += FONT_MODS["B"] if b else ""
    return f"{mods}{repr(data)}{FONT_MODS['ENDC']}"


def joinsep(l, sep=", ", caps="__repr__"):
    return sep.join([getattr(x, caps)() for x in l])


def safe_dump_json(data: object) -> str:
    default = lambda o: f"{type(o).__qualname__}: {str(o)}"
    return json.dumps(data, default=default)


def safe_dump_yaml(data, file):
    with open(file, "w") as f:
        yaml.dump(data, f, default_flow_style=False, sort_keys=False)


def is_iterable(obj):
    try:
        iter(obj)
        return True
    except:
        return False


def fmt_data(data, fmt):
    """Formats data input to given output format
    Options:
    * str: Simply dump the data to its str() representation
    * yaml: Dump data to yaml. Be careful, yaml will serialize the whole data tree, often resulting in a mess
    * json: Dump data to json. Data may be truncated as json only dumps basic data structures (dict, list)
    * pretty: Return pformat(data). Trys to pretty-print python objects
    """
    if fmt is None:
        return data
    try:
        if fmt == "pretty":
            data = pformat(data)
        if fmt == "str":
            data = str(data)
        if fmt in ["yaml", "yml"]:
            data = yaml.dump(data, sort_keys=False)
        if fmt == "jsonl":
            if is_iterable(data):
                data = [safe_dump_json(i) for i in data]
            else:
                data = safe_dump_json(data)
        if fmt == "json":
            data = safe_dump_json(data)
        if isinstance(data, (minidom.Element, minidom.Document)):
            data = data.toprettyxml(indent="  ").replace("\n\n", "")
        # if isinstance(data, (dict,)):
        #     data = str(data)
    except Exception as e:  # If something goes wrong:
        log.debug(f"{fmt}: {data}")  # Log format, data and error
        log.error(repr(e))
        data = str(data)
    return data  # Return data, formatted or not


def format_return(default_format: str = None) -> Callable:
    def format_return_decorator(func: Callable) -> Callable:
        """
        Format output of the decorated method
        This decorator looks for the keyword "fmt" in the decorated method and returns the formatted output.
        """
        # @functools.wraps(func, updated=())  # Preserves function attributes, e.g. __doc__
        def format_return_wrapper(self="None", *args, **kwargs) -> Any:
            fmt = kwargs.get("fmt", default_format)  #  Find "fmt" in kwargs
            data = func(self, *args, **kwargs)  #  Store method output in data
            cls = self.__class__.__name__ if isinstance(self, object) else __name__
            log.debug(f"{cls}.{func.__name__}{args}, {kwargs}")
            return fmt_data(data, fmt) if fmt else data

        # Preserve function docstring
        format_return_wrapper.__doc__ = func.__doc__
        return format_return_wrapper

    return format_return_decorator


def i2b2_password_cryptor(password: str) -> str:
    """Return hash from plain password according to i2b2 database hash

    Hash pw with md5 and do a bitwise AND operation on 255 (0x00FF) with each char
    Algorithm copied from "I2b2PasswordCryptor.java":
    https://open.catalyst.harvard.edu/stash/projects/SHRINE/repos/shrine/browse/install/i2b2-1.7/i2b2/I2b2PasswordCryptor.java?at=dfeb7073273003a3ffa30334ef58db50106d56ec
    """
    m = hashlib.md5()
    m.update(password.encode(encoding="utf-8"))
    hexdigest = ""
    for char in m.digest():
        # Get numerical value
        char_as_int = int(char)
        # AND-combine value with 255
        and_combined = char_as_int & 0x00FF
        # Convert to hex
        as_hex = hex(and_combined)
        # Cut "0x" off the string
        as_hex = as_hex[2:]
        hexdigest += as_hex
    return str(hexdigest)


def pg_db_string(
    user: str = "postgres",
    password: str = "postgres",
    host: str = "localhost",
    port: int = 5432,
    database: str = "public",
):
    return f"postgresql://{user}:{password}@{host}:{port}/{database}"


# XML STUFF
# ----------
def xml_set_namespace(doc: minidom.Element, namespace: str) -> minidom.Document:
    el = doc.createElementNS(namespace, "datasources")
    el.setAttribute("xmlns", namespace)
    doc.appendChild(el)
    return doc


def prettyxml(doc: minidom.Document):
    raw = doc.toprettyxml(encoding="utf-8").splitlines()
    raw = os.linesep.join([s.decode("utf-8") for s in raw if s.strip()])
    return raw


def xml_file_dump(file_path: str, doc: minidom.Document) -> str:
    backup_file(file_path)
    # raw = doc.toprettyxml(encoding="utf-8").splitlines()
    # raw = os.linesep.join([s.decode("utf-8") for s in raw if s.strip()])
    raw = prettyxml(doc)
    with open(file_path, "w", encoding="utf-8") as write_file:
        write_file.write(raw)
    return file_path


## RUN STUFF  ##
def docker_exec(container, cmd, opts=""):
    base = f'''docker exec {opts} -it {container} bash -c "{cmd}"'''
    for out, err, ret in run(base):
        log.info(f"{out}")
        log.warning(f"{err}") if err else None


def psql(db_string, cmd, file=True, prefix="", data=None):
    vars = " ".join([f'-v {k}="{v}"' for k, v in data.items()]) if data else ""
    cmd = f'psql {prefix} {db_string} {vars}  -{"f" if file else "c"} "{cmd}"'
    return execute(cmd, split=False)


def run(cmd: str) -> tuple:
    process = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
    while True:
        out = process.stdout.readline().rstrip().decode("utf-8")
        err = process.stderr.readline().rstrip().decode("utf-8")
        # ret = None
        ret = process.wait()
        if not out and not err:
            break
        yield out, err, ret


def cmd_to_list(cmd: str):
    out_lines, err_lines = []
    for out, err in run(cmd):
        out_lines += out
        err_lines += err


def vrun(cmd: str):
    ret = None
    for out, err, ret in run(cmd):
        print(f"{out}")  # if err else None
        print(f"{err} {ret if ret else ''}") if err else None


def execute(cmd="uname -a", split=True) -> list:
    """
    Execute command and return stdout, stderr and exit code
    Args:
        cmd (str): CLI command, will be split to list of flags
    Returns:
        List: [output (bytestring), error (bytestring), exit code (int)]
    """
    cmd = cmd.split(" ") if split else cmd
    log.info(f"CMD: {cmd}")
    process = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
    out, err = process.communicate()
    return_code = process.returncode
    return [out.decode(), err.decode(), return_code]


# FOLDERS AND FILES
# ------------------
def find_files(d, ext=None):
    files = []
    for path in os.scandir(d):
        if path.is_file():
            if ext:
                if path.name.endswith(ext):
                    files.append(path)
            else:
                files.append(path)
        if path.is_dir():
            files += find_files(path, ext=ext)
    return files


def backup_file(file: str, ext: str = ".bak", fail=False):
    try:
        shutil.copy(file, file + ext, follow_symlinks=True)
    except Exception as err:
        if fail:
            raise err


def copy_folder(source, target, overwrite=False):
    path_exists = os.path.isdir(target)
    if path_exists and overwrite is True:
        shutil.rmtree(target)
    if path_exists and overwrite is False:
        raise FileExistsError(target)
    shutil.copytree(source, target)
    return target


# HELPER CLASSES
# ---------------
class SQLException(Exception):
    """Dummy Class for SQL related Errors"""


class GetData:
    def __init__(self, data: dict = None, name=None):
        self.data = data
        self.name = name

    @format_return("yaml")
    def show(self, fmt=None):
        return self

    def get(self, dot_path: str, default: object = None):
        data = self.data
        for i in dot_path.split("."):
            try:
                data = data[i]
            except KeyError as err:
                log.debug(f"GetData: {repr(err)} -> default '{default}'")
                if default is not None:
                    return default
                raise err
        return data

    def __getitem__(self, item):
        return self.data[item]

    def __repr__(self):
        return repr(self.data)


class Singleton:
    def __init__(self, cls):
        self.cls = cls
        self.instance = None

    def __call__(self, *args, **kwargs):
        if self.instance is None:
            self.instance = self.cls(*args, **kwargs)
        stack = inspect.stack()
        the_class = stack[1][0].f_locals["self"].__class__.__name__
        the_method = stack[1][0].f_code.co_name
        this_class = self.instance.__class__.__name__
        log.debug(f"{this_class}: {the_class}.{the_method}()")
        return self.instance
