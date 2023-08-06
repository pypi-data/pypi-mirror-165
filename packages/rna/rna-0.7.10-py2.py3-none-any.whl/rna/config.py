"""
A generic interface for configuration setups using different
 dialects (e.g. cfg, ini, toml, json, etc.).
It allows to provide multiple configuration file locations wich are searched
 in the order they are given for a configuration option.
Also there is the option for falling back a hirarchy level above
 the section requested for "config inheritance".
Dynamic options and links are possible as well.
"""
from modulefinder import Module
import types
import typing
from abc import abstractmethod
import os
import re
import pathlib

import rna.path
from rna.pattern.strategy import Context, Strategy


OPTION_NOT_FOUND = object()


def _split_keys(*args) -> typing.Tuple:
    """
    Examples:
        >>> _split_keys("section.subsection", "option")
        ('section', 'subsection', 'option')
        >>> _split_keys("section", "subsection", "option.suboption")
        ('section', 'subsection', 'option', 'suboption')
    """
    new_args = []
    for arg in args:
        if "." in arg:
            new_args.extend(arg.split("."))
        else:
            new_args.append(arg)
    return tuple(new_args)


class Dialect(Strategy):
    """
    Abstract Class to be derived by specific dialects of a config files (.ini, .cfg, ...)
    """

    def __init__(self):
        super().__init__()
        self._config_cache = {}

    def _get_config(self, config_path) -> "configparser.ConfigParser":
        """
        Retrieve a .cfg config file
        """
        if config_path not in self._config_cache:
            if os.path.exists(config_path):
                config = self._load_config(config_path)
                self._config_cache[config_path] = config
            else:
                self._config_cache[config_path] = None
        return self._config_cache[config_path]

    @abstractmethod
    def _load_config(self, config_path: str) -> typing.IO:
        """
        Return the loaded config file. The config file will not be checked for existence.
        """

    @abstractmethod
    def get(self, config_path, *keys: str, fallback=False) -> any:
        """
        Retrieve the value corresponding to the keys from the config file referred by config_path.

        Returns:
            Any or OPTION_NOT_FOUND flag if option or section not found.
        """

    @staticmethod
    def prepare_keys(*keys: str) -> typing.Tuple[str]:
        """
        Prepare keys for get(). Usually splitting along "." and removing empty strings.

        Examples:
            >>> Dialect.prepare_keys("section.subsection", "option")
            ('section', 'subsection', 'option')
            >>> Dialect.prepare_keys("section", "subsection", "option.suboption")
            ('section', 'subsection', 'option', 'suboption')
        """
        return tuple(filter(None, re.split(r"\.", ".".join(keys))))


class TomlParser(Dialect):
    """
    Parser flavour for the '.toml' dialect.
    """

    @staticmethod
    def _load_config(config_path: str) -> dict:
        with open(config_path) as _file:
            import toml

            return toml.load(_file)

    def get(self, config_path, *keys: str):
        """
        Abstract method, derived from :meth:`Dialect.get`:
        """
        config = self._get_config(config_path)
        if config is None:
            return OPTION_NOT_FOUND
        depth = len(keys)
        for i in range(depth):
            key = keys[i]
            if key not in config:
                return OPTION_NOT_FOUND
            config = config[key]
        return config


class ConfigParser(Dialect):
    """
    Parser flavour for the '.config' dialect.
    """
    def __init__(self, *args, **kwargs):
        # import only when needed
        global configparser
        import configparser

        super().__init__(*args, **kwargs)

    def _load_config(self, config_path: str) -> "configparser.ConfigParser":
        config = configparser.ConfigParser()  # pylint:disable=undefined-variable
        config.read(config_path)
        return config

    def get(self, config_path, *keys: str):
        """
        Abstract method, derived from :meth:`Dialect.get`:
        """
        config_path = self._get_config(config_path)
        try:
            val = self.get(config_path, *keys)
            return val
        # pylint:disable=undefined-variable
        except (configparser.NoOptionError, configparser.NoSectionError):
            return OPTION_NOT_FOUND


class Config(Context):
    """
    Central config class for handling multiple config files (different permissions,
    locations, fallback, ...) that combine to one config for a project.
    Can be used with different dialects (e.g. cfg, ini, toml, json, etc.) - implemented
    with the Strategy pattern.

    Args:
        *config_paths: paths to config files to load. When searching an option in a config
             file, the config file with the highest priority (leftmost file) is searched first.
        dynamic_variables_regex: regex used to replace matching occurences in string values
             by retrieved by :meth:`get`: by (filled with **variables).
        **variables: values are replacing matches in strings retrieved by :meth:`get`:

    Examples:
        >>> import rna
        >>> import rna.config
        >>> config = rna.config.Config(
        ...     "path/to/config/file/to/be/searched/first/user.toml",
        ...     "path/to/fallback/user.toml",
        ...     "path/to/fallback/of/fallback/config.toml",
        ...     INSERT_THIS="Hello",
        ... )

        >>> config.set("database.backup.path", "$INSERT_THIS world!")
        >>> assert config.get("database.backup.path") == "Hello world!"
    """
    STRATEGY_TYPE = Dialect
    DIALECTS = []

    @classmethod
    def register_dialect(
        cls,
        dialect: typing.Type[Dialect],
        extension: typing.Union[str, typing.Tuple[str]],
    ):
        """
        Register a dialect for a file extension.
        """
        if isinstance(extension, tuple):
            for ext in extension:
                cls.register_dialect(dialect, ext)
            return
        assert issubclass(dialect, Dialect)
        cls.DIALECTS.append((extension, dialect))

    @classmethod
    def api(cls, module: typing.Union[Module, str], *args, dialect="toml", **variables):
        """
        Create a Config instance that is a proper default for an api.
        It has paths set for user and default config files.

        Args:
            module: Module or path to the __init__.py of the module
             (intended use is to call this from the module's __init__.py
              and pass __file__ as argument).
            *args: forwards to Config.__init__
            dialect: extension of the config files, indicating the dialect to use
            **variables: forwards to Config.__init__

        """
        if isinstance(module, types.ModuleType):
            module_name = module.__name__
            module_path = module.__path__[0]
        else:
            assert os.path.basename(module) == "__init__.py"
            module_name = module.split(os.path.sep)[-2]
            module_path = os.path.dirname(module)

        variables.setdefault("HOME", rna.path.resolve("~"))
        variables.setdefault("MODULE", module_path)
        return cls(
            rna.path.resolve("~", f".{module_name}", f"local.{dialect}"),
            rna.path.resolve("~", f".{module_name}", f"config.{dialect}"),
            rna.path.resolve(module_path, f"config.{dialect}"),
            *args,
            **variables,
        )

    def __init__(
        self,
        *config_paths,
        dynamic_variables_regex=r"[^${\}]+(?=})",
        strategy=None,
        **variables,
    ):

        self._config_paths = config_paths
        self._variables = variables
        self._dynamic_variables_regex = dynamic_variables_regex
        self._dynamic_options = {}
        if strategy is None and config_paths and self.DIALECTS:
            ext = os.path.splitext(config_paths[0])[1]
            for dialect_ext, dialect in self.DIALECTS:
                if ext == dialect_ext:
                    strategy = dialect
                    break
        super().__init__(strategy=strategy)

    def set(self, *keys_and_value: typing.Union[str, any]):
        """
        Dynamically set an option. This option can be removed with reset().

        Args:
            *keys_and_value: keys and value of the option.
                value must be the last argument.
        """
        keys = keys_and_value[:-1]
        value = keys_and_value[-1]
        remaining = self.strategy.prepare_keys(*keys)
        obj = self._dynamic_options
        while remaining:
            # a part is a section or subsection
            part = remaining[0]
            remaining = remaining[1:]
            if remaining:
                if part not in obj:
                    obj[part] = {}
                obj = obj[part]
            else:
                # the last part remains (option)
                obj[part] = value

    def _get_dynamic_option(self, *keys: str):
        """
        Returns:
            dict of dynamic options or the value of the option if it is a leaf
        """
        obj = self._dynamic_options
        remaining = keys
        while remaining:
            # a part is a section or subsection
            part = remaining[0]
            remaining = remaining[1:]
            obj = obj[part]
        return obj

    def reset(self, *keys: str):
        """
        Remove dynamic option from dynamic option cache and reset to config file retrievement.
        """
        keys = self.strategy.prepare_keys(*keys)
        sections = keys[:-1]
        option = keys[-1]
        obj = self._get_dynamic_option(*sections)
        del obj[option]

    def get(self, *keys: str, fallback=False):
        """
        Retrieve option from section.
        Dynamic variables in values are resolved. Syntax:
            ${section.subsection.key}: variable forwarded to get(section, subsection, key)
            $VARIABLE: replacing VARIABLE with the value of the variable set at init time.

        Args:
            keys: section (and subsections if multiple) in config file
            fallback: if option not found in specified (sub) section, fall back to parent section
                (removing one level indicated by dot separators)
        """
        keys = self.strategy.prepare_keys(*keys)

        # dynamic option has highest priority
        val = OPTION_NOT_FOUND
        try:
            val = self._get_dynamic_option(*keys)
        except KeyError:
            pass

        if val is OPTION_NOT_FOUND:
            for config_path in self._config_paths:
                val = self.strategy.get(config_path, *keys)
                if val is not OPTION_NOT_FOUND:
                    break

        if val is not OPTION_NOT_FOUND and isinstance(val, str):
            # replace explicit mentions of VARIABLES
            for env_var, env_value in self._variables.items():
                val = val.replace("$" + env_var, env_value)

            # replace by regex with recursive get_option in value
            matches = re.finditer(self._dynamic_variables_regex, val)
            for match in reversed(list(matches)):
                start, end = match.span()
                # recursively replace the match by get_option
                val = (
                    val[: start - 2]
                    + self.get(*match.group().rsplit(".", 1))
                    + val[end + 1 :]
                )
        elif val is OPTION_NOT_FOUND and fallback and len(keys) > 1:
            keys = keys[:-2] + keys[-1:]
            val = self.get(*keys, fallback=fallback)

        if val is OPTION_NOT_FOUND:
            raise KeyError(keys)

        return val

    def get_path(self, *keys, **kwargs) -> pathlib.Path:
        """
        Format a config field as pathlib.Path. This allows converting paths for your system.

        Note:
            We propose to use posix separators ("/") even in windows paths since they are forbidden
            characters in windows paths and are thus clear indicators of separators.
            Windows Network paths should still use the windows separator. A Network path under
             windows would look like this in your config file: "\\\\asdf-sdf/path/to/thing.txt".
            Same goes for Drive letters ("C:\\Users/Appdata/thing.txt")
        """
        path = self.get(*keys, **kwargs)
        wsep = pathlib.WindowsPath._flavour.sep
        psep = pathlib.PosixPath._flavour.sep
        if psep in path:
            # PosixPath given. Save to assume since "/" is forbidden in windows paths
            if pathlib._WindowsFlavour.is_supported:
                # convert posix to windows
                val = pathlib.Path(*path.split(wsep))
            else:
                val = pathlib.Path(path)
        elif wsep in path:
            # WindowsPath given (assumed - could be posix still but is less likely)
            if pathlib._WindowsFlavour.is_supported:
                val = pathlib.Path(path)
            else:
                # convert windows to posix
                val = pathlib.Path(*path.split(psep))
        else:
            val = pathlib.Path(path)
        return val


Config.register_dialect(ConfigParser, (".cfg", ".ini"))
Config.register_dialect(TomlParser, ".toml")
