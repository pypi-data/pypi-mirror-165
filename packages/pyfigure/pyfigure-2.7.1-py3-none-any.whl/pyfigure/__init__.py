from pathlib import Path
from typing import Callable, Any, Tuple
from dataclasses import dataclass
from sys import argv
from inspect import isclass
from tomlkit import load, dump, table
from typeguard import check_type
from superdict import SuperDict

class Config:
    """Declare config options."""

@dataclass
class Option:
    default: Any
    description: str = ''
    type: Any = Any

class ParseError(Exception):
    def __init__(self, *args, original_error: Exception()):
        self.original_error = original_error
        super().__init__(*args)

class CheckError(ParseError):
    pass

class Configurable:
    """Create configuration files from classes.

    Attributes:
        config: A dictionary containing all of the parsed values from the class' configuration file.
        config_file: The Path object of the configuration file. 
    """

    config: SuperDict
    config_file: Path

    def __init__(self,
        manual_errors: bool = False
    ):
        self.config = SuperDict()
        self.manual_errors = manual_errors

        if not hasattr(self, 'config_file'):
            executed_file = Path(argv[0])
            self.config_file = executed_file.with_suffix('.toml')
        if not isinstance(self.config_file, Path):
            self.config_file = Path(self.config_file)

        self.reload_config()

    def reload_config(self):
        """(Re)load the config option."""
        _defaults = {}
        for config in self._get_nested_configs():
            _defaults.update(self.generate_defaults(config))
        if hasattr(self, 'Config'):
            _defaults.update(self.generate_defaults(self.Config))
        if not _defaults:
            return

        if self.config_file.exists() and self.config_file.stat().st_size > 0:
            with open(self.config_file, 'r') as file:
                data = load(file)
            self.load_config(data, _defaults, self.config)
            self.config, updated = self.fill_config(_defaults, self.config)
            if updated:
                with open(self.config_file, 'w+') as file:
                    document = self.document_from_config(_defaults, self.config)
                    dump(document, file)
        else:
            self.config = self.generate_config(_defaults)
            with open(self.config_file, 'w+') as file:
                document = self.document_from_config(_defaults, self.config)
                dump(document, file)

        self.config = self.parse_config(_defaults, self.config)

        del _defaults

    def _get_nested_configs(self):
        result = []
        for name in dir(self):
            if not hasattr(self, name): continue
            obj = getattr(self, name)
            if isclass(obj) and issubclass(obj, Config):
                result.append(obj)
        return result

    def generate_defaults(self, config: dict, defaults: dict = None):
        """Generate config defaults from classes."""

        if not defaults: defaults = {}
        values = dict(config.__dict__)
        types = values.get('__annotations__', {})

        # remove internal values
        for key, _ in values.copy().items():
            if key.startswith('__'):
                del values[key]

        for key, value in values.items():

            if isinstance(value, Option):
                defaults[key] = value
                if key in types:
                    defaults[key].type = types[key]
                else:
                    defaults[key].type = Any
            elif isclass(value):
                if key not in types: types[key] = {}
                defaults[value.__name__] = self.generate_defaults(values[key], types[key])
            elif isinstance(value, dict):
                raise TypeError("Dictionary options are currently not functional, please use a list of dictionaries or a config subgroup instead.")
            else:
                raise TypeError("Config values must be Option objects")
        
        return defaults

    def load_config(self, data, defaults, config):
        """Load a locally saved config."""
        for key, value in data.items():
            if key not in defaults:
                continue
            if isinstance(value, dict):
                config[key] = SuperDict()
                value = self.load_config(value, defaults[key], config[key])
            if not isinstance(value, bool):
                value = value.value
            config[key] = value

        return config


    def document_from_config(self, defaults: dict, config: dict) -> table():
        """Turn a config into a TOML Document with comments."""
        document = table()

        for key, value in defaults.items():
            
            if isinstance(value, dict):
                document[key] = self.document_from_config(defaults[key], config[key])
            else:
                document[key] = config[key]#.__repr__()
                if value.description:
                    document.value.item(key).comment(value.description)

        return document

    def fill_config(self, defaults: dict, config: dict) -> Tuple[dict, bool]:
        """Fill a config if it has missing default values."""
        updated = False

        for key, value in defaults.items():

            if isinstance(value, dict):
                if key not in config: config[key] = {}
                sub, sub_up = self.fill_config(defaults[key], config[key])
                updated = updated or sub_up
                if sub: config[key] = sub

            elif key not in config:
                config[key] = value.default
                updated = updated or True

        return config, updated

    def generate_config(self, defaults: dict, config: dict = None) -> dict:
        """Generate a config from defaults."""
        if not config: config = {}

        for key, value in defaults.items():

            if isinstance(value, dict):
                config[key] = self.generate_config(defaults[key])
            else:
                config[key] = value.default
        
        return config

    def parse_config(self, defaults: dict, config: dict) -> dict:
        """Parse config values and check types."""
        # go over every value in the config

        for key, value in config.items():

            # if the value isn't in the default values, ignore it
            if key not in defaults:
                continue

            default_data = defaults[key]

            # if dict, loop over it
            if isinstance(value, dict):
                value = self.parse_config(default_data, value)
                continue

            try:
                value = self.parse_value(key, value, default_data)
            except (ParseError, CheckError) as error:
                value = self.parse_value(key, default_data.default, default_data)
                if self.manual_errors:
                    raise error
                print(error)
    
            config[key] = value
            
        return config

    def parse_value(self, key, value, default_data):


        if default_data.type != Any:

            try:
                value = default_data.type(value)
            except ValueError as parse_error:
                raise ParseError(f"Error while trying to parse option '{key}': {str(parse_error)}", original_error=parse_error) from parse_error
            except TypeError:
                pass
            return value

        try:
            check_type(key, value, default_data.type)
        except TypeError as check_error:
            raise CheckError(f"Error while trying to load option '{key}': {str(check_error)}", original_error=check_error) from check_error

        return value