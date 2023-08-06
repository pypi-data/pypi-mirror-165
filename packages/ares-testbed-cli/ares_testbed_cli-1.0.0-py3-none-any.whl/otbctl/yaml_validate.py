from schema import Schema, SchemaError, Or
import yaml
from .log_management import log_management

infoDualLogger = log_management.get_info_dual_logger()
errorDualLogger = log_management.get_error_dual_logger()

# stricter requirements can be enacted for any str, using regex or Schema
config_schema = Schema({
    "version": float,
    "workflows": Or([{ # type for "workflows" can be list or dict
        "flow": { 
            "source": {
                "auth-endpoint": str,
                # specific error messages are provided to user as such:
                "auth-type": Or("Token", error="auth-type must be 'Token'."),
                "method": Or("POST", "GET", error="method must be 'POST' or 'GET'."),
                "isAuthOnly": Or(bool, error="isAuthOnly must be True or False."),
                "headers": [{object: object}],
                "request": {
                    "api-endpoint": str,
                    "method": Or("POST", "GET", "None"),
                    "auth-type": "Bearer",
                    "token-name": "access_token",
                    "headers": [{object: object}],
                    "params": Or([{object: object}], None),
                    "body": str
                }
            },
            "testbed": {
                "request": {
                    "method": Or("POST", "GET"),
                    "status": 200,
                    "path": str,
                    "params": Or([{object: object}], None),
                    "headers": [{object: object}],
                    "body": Or({
                        "matcher": Or("ShouldEqual", "ShouldMatch", "ShouldEqualJSON", "ShouldContainSubstring"),
                        "value": str
                    }, str)
                }
            }
        }
    }], { 
        "flow": { # accounts for "workflows" as dict
            "source": {
                "auth-endpoint": str,
                # specific error messages are provided to user as such:
                "auth-type": Or("Token", error="auth-type must be 'Token'."),
                "method": Or("POST", "GET", error="method must be 'POST' or 'GET'."),
                "isAuthOnly": Or(bool, error="isAuthOnly must be True or False."),
                "headers": [{object: object}],
                "request": {
                    "api-endpoint": str,
                    "method": Or("POST", "GET", "None"),
                    "auth-type": "Bearer",
                    "token-name": "access_token",
                    "headers": [{object: object}],
                    "params": Or([{object: object}], None),
                    "body": str
                }
            },
            "testbed": {
                "request": {
                    "method": Or("POST", "GET"),
                    "status": 200,
                    "path": str,
                    "params": Or([{object: object}], None),
                    "headers": [{object: object}],
                    "body": Or({
                        "matcher": Or("ShouldEqual", "ShouldMatch", "ShouldEqualJSON","ShouldContainSubstring"),  
                        "value": str   
                    },str)
                }
            }
        }
    }
)})

def validate_config(config_yaml):
    with open(config_yaml, 'r') as f:
        file_to_check = yaml.safe_load(f)
    try:
        config_schema.validate(file_to_check)
        infoDualLogger.info("YAML follows valid pattern")
        return config_yaml
    except SchemaError as se:
        errorDualLogger.error("YAML needs changes: ")
        for error in se.errors:
            if error:
                errorDualLogger.error(error)
        for error in se.autos:
            if error:
                errorDualLogger.error(error)
        exit()