from schema import Schema, SchemaError, Optional
from yaml.scanner import ScannerError
from yaml.parser import ParserError
import yaml
import syslog

nodes_schema = Schema([{
    "address": str,
    "port": int,
    "key": str
}])

conf_schema = Schema({
    "email": str,
    "password": str,
    "server": str,
    "subject": str,
    "time_in_hours": int,
    Optional("nodes"): nodes_schema
})

def get_config_object():
    try:
        file_obj = open("/etc/lacs.yaml", "r")
        result = yaml.safe_load(file_obj)
        if conf_schema.is_valid(result):
            return conf_schema.validate(result)
        else:
            syslog.syslog(syslog.LOG_CRIT, "Config file not Valid. Check for proper types and required fields.")
    except FileNotFoundError as e:
        syslog.syslog(syslog.LOG_CRIT, "Config file not found.")
        exit(1)
    except ScannerError as e:
        syslog.syslog(syslog.LOG_CRIT, "YAML scanner error when trying to load config")
        exit(1)
    except ParserError as e:
        syslog.syslog(syslog.LOG_CRIT, "YAML Parser error: check config syntax.")
        exit(1)