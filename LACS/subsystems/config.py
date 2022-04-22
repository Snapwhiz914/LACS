from schema import Schema, SchemaError, Optional
from yaml.scanner import ScannerError
from yaml.parser import ParserError
import yaml
import imaplib
import sys

nodes_schema = Schema([{
    "address": str,
    "port": int,
    "key": str
}])

conf_schema = Schema({
    "email": str,
    "password": str,
    "server": str,
    "port": int,
    "subject": str,
    "time_in_hours": int,
    Optional("nodes"): nodes_schema
})

def check_if_server_is_reachable(server, port):
    try:
        imaplib.IMAP4_SSL(host=server, port=port)
    except Exception as e:
        print(f"Could not connect to email server with error: {e}")
        sys.exit(1)

def get_config_object():
    try:
        file_obj = open("/etc/lacs.yaml", "r")
        result = yaml.safe_load(file_obj)
        validated = conf_schema.validate(result)
        check_if_server_is_reachable(validated["server"], validated["port"])
        return validated
    except FileNotFoundError as e:
        print("Config file not found.")
        sys.exit(1)
    except ScannerError as e:
        print(f"YAML scanner error when trying to load config: {e}")
        sys.exit(1)
    except ParserError as e:
        print(f"YAML Parser error: check config syntax: {e}")
        sys.exit(1)