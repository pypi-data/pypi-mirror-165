import collections
import configparser
import errno
import os
import re

import aiobtclientapi
from xdg.BaseDirectory import xdg_config_home

from . import __project_name__, _errors

from . import _debug  # noqa:F401 isort:skip


DEFAULT_LOCATIONS_FILEPATH = os.path.join(xdg_config_home, __project_name__, 'locations')
DEFAULT_CLIENTS_FILEPATH = os.path.join(xdg_config_home, __project_name__, 'clients.ini')


class Locations(collections.abc.MutableSequence):
    """
    :class:`list` subclass that reads directory paths from `filepath`

    :param locations: Directory paths
    :param filepath: File to read more `locations` from

    The format of `filepath` is very simple:

        * Directory paths are separated by newlines.

        * Lines that start with "#" and empty lines are ignored.

        * If a path ends with ``f"{os.sep}*"``, all subdirectories in that
          directory are added.

        * Basic environment variable expansion is supported, e.g. "$HOME/foo".

    :raise ConfigError: if reading `filepath` fails or if it contains a file
        path
    """

    def __init__(self, *locations, filepath):
        self._filepath = filepath
        self._list = []
        # self.extend() should normalize `locations`. _read() does that on its
        # own and provides the proper filepath and line_number to ConfigError.
        self.extend(locations)
        self._list.extend(self._read(filepath))

    @property
    def filepath(self):
        return self._filepath

    def __repr__(self):
        return f'<{type(self).__name__} {self._filepath!r} {self._list!r}>'

    def _read(self, filepath):
        locations = []

        try:
            with open(filepath, 'r') as f:
                for line_number, line in enumerate(f.readlines(), start=1):
                    line = line.strip()
                    if line and not line.startswith('#'):
                        for normalized_path in self._normalize(line, filepath, line_number):
                            if normalized_path not in locations:
                                locations.append(normalized_path)

        except OSError as e:
            # Ignore missing default config file path
            if e.errno == errno.ENOENT and filepath == DEFAULT_LOCATIONS_FILEPATH:
                pass
            else:
                msg = e.strerror if e.strerror else str(e)
                raise _errors.ConfigError(f'Failed to read: {msg}', filepath=filepath)

        return locations

    @classmethod
    def _normalize(cls, line, filepath, line_number):
        subdirs = []

        if line.endswith(f'{os.sep}*'):
            # Expand "*"
            parent_dir = line[:-2]
            try:
                subdir_names = os.listdir(parent_dir)
            except OSError as e:
                msg = e.strerror if e.strerror else str(e)
                raise _errors.ConfigError(f'Failed to read subdirectories from {parent_dir}: {msg}',
                                          filepath=filepath, line_number=line_number)
            else:
                for name in subdir_names:
                    subdir_path = os.path.join(parent_dir, name)
                    # Exclude non-directories (files and exotic stuff like
                    # sockets), but include nonexisting paths (subdir_path may
                    # contain unresolved environment variables and download
                    # locations may not exist anyway)
                    if os.path.isdir(subdir_path) or not os.path.exists(subdir_path):
                        subdirs.append(subdir_path)
        else:
            subdirs.append(line)

        # Resolve environment variables
        subdirs = [
            cls._resolve_env_vars(subdir, filepath, line_number)
            for subdir in subdirs
        ]

        # Complain if subdir exists but is not a directory
        for subdir in subdirs:
            if os.path.exists(subdir) and not os.path.isdir(subdir):
                raise _errors.ConfigError(f'Not a directory: {subdir}',
                                          filepath=filepath, line_number=line_number)

        return sorted(subdirs)

    @classmethod
    def _resolve_env_vars(cls, line, filepath, line_number):
        # Resolve "~/foo" and "~user/foo"
        path = os.path.expanduser(line)

        while True:
            # Find valid variable name
            # https://stackoverflow.com/a/2821201
            match = re.search(r'\$([a-zA-Z_]+[a-zA-Z0-9_]*)', path)
            if not match:
                break
            else:
                env_var_name = match.group(1)
                env_var_value = os.environ.get(env_var_name, None)
                if env_var_value is None:
                    raise _errors.ConfigError(f'Unset environment variable: ${env_var_name}',
                                              filepath=filepath, line_number=line_number)
                elif env_var_value == '':
                    raise _errors.ConfigError(f'Empty environment variable: ${env_var_name}',
                                              filepath=filepath, line_number=line_number)
                else:
                    path = path.replace(f'${env_var_name}', env_var_value)

        return path

    def __setitem__(self, index, value):
        # `index` can be int or slice and `value` can be one path or list of
        # paths.
        if not isinstance(value, str) and isinstance(value, collections.abc.Iterable):
            normalized_paths = []
            for item in value:
                for normalized_path in self._normalize(item, None, None):
                    if normalized_path not in self._list:
                        normalized_paths.append(normalized_path)
            self._list[index] = normalized_paths

        else:
            normalized_path = self._normalize(value, None, None)[0]
            if normalized_path not in self._list:
                self._list[index] = normalized_path

    def insert(self, index, value):
        normalized_paths = self._normalize(value, None, None)
        self._list.insert(index, normalized_paths[0])

    def __getitem__(self, index):
        return self._list[index]

    def __delitem__(self, index):
        del self._list[index]

    def __len__(self):
        return len(self._list)

    def __eq__(self, other):
        if isinstance(other, collections.abc.Sequence):
            return self._list == list(other)
        else:
            return NotImplemented


class Clients(collections.abc.Mapping):
    """
    :class:`dict` subclass that reads BitTorrent client configs from INI file

    :param filepath: File to read client configurations from

    :raise ConfigError: if reading `filepath` fails or if it contains a file
        path
    """

    def __init__(self, filepath):
        self._filepath = filepath
        self._config = self._read(filepath)

    def _read(self, filepath):
        cfg = configparser.ConfigParser(
            default_section=None,
            interpolation=None,
            allow_no_value=False,
            delimiters=('=',),
            comment_prefixes=('#',),
        )
        try:
            cfg.read_string(
                open(filepath, 'r').read(),
                source=filepath,
            )
        except OSError as e:
            # Ignore missing default config file path
            if e.errno != errno.ENOENT or filepath != DEFAULT_CLIENTS_FILEPATH:
                msg = e.strerror if e.strerror else str(e)
                raise _errors.ConfigError(f'Failed to read: {msg}', filepath=filepath)
        except configparser.MissingSectionHeaderError as e:
            raise _errors.ConfigError(f'Line {e.lineno}: {e.line.strip()}: Option outside of section', filepath=filepath)
        except configparser.ParsingError as e:
            lineno, msg = e.errors[0]
            raise _errors.ConfigError(f'Line {lineno}: {msg.strip()}: Invalid syntax', filepath=filepath)
        except configparser.DuplicateSectionError as e:
            raise _errors.ConfigError(f'Line {e.lineno}: {e.section}: Duplicate section', filepath=filepath)
        except configparser.DuplicateOptionError as e:
            raise _errors.ConfigError(f'Line {e.lineno}: {e.option}: Duplicate option', filepath=filepath)
        except configparser.Error as e:
            raise _errors.ConfigError(str(e), filepath=filepath)

        # Validation
        dct = self._as_dict(cfg)
        self._ensure_only_valid_options(filepath, dct)
        self._ensure_mandatory_options(filepath, dct)
        self._fill_in_defaults(dct)
        self._convert_values(filepath, dct)
        return dct

    def _as_dict(self, cfg):
        return {
            section: dict(cfg.items(section))
            for section in cfg.sections()
        }

    _valid_options = (
        'client',
        'url',
        'username',
        'password',
        'verify',
        'stopped',
    )

    def _ensure_only_valid_options(self, filepath, dct):
        for section in dct:
            for option in dct[section]:
                if option not in self._valid_options:
                    raise _errors.ConfigError(f'{section}: Unknown option: {option}', filepath=filepath)

    _mandatory_options = ('client',)

    def _ensure_mandatory_options(self, filepath, dct):
        for section in dct:
            for option in self._mandatory_options:
                if option not in dct[section]:
                    raise _errors.ConfigError(f'{section}: Missing option: {option}', filepath=filepath)

    _defaults = {
        # Empty URL means "default URL" when passed to one of the
        # aiobtclientapi.*API.URL classes (see _convert_to_url())
        'url': '',
        'username': '',
        'password': '',
        'verify': False,
        'stopped': False,
    }

    # Client-specific defaults
    _client_defaults = collections.defaultdict(
        lambda: collections.defaultdict(lambda: None),
        {
            'transmission': collections.defaultdict(
                lambda: None,
                {
                    # Transmission can't add torrents without verifying
                    'verify': True,
                },
            ),
        },
    )

    def _fill_in_defaults(self, dct):
        for section in dct:
            for option in self._defaults:
                if option not in dct[section]:
                    client_name = dct[section]['client']
                    client_default_value = self._client_defaults[client_name][option]
                    if client_default_value is not None:
                        dct[section][option] = client_default_value
                    else:
                        dct[section][option] = self._defaults[option]

    def _convert_values(self, filepath, dct):
        convert_map = {
            'client': self._convert_to_client,
            'url': self._convert_to_url,
            'verify': self._convert_to_bool,
            'stopped': self._convert_to_bool,
        }
        for section, options in dct.items():
            for option, converter in convert_map.items():
                try:
                    options[option] = converter(options, option)
                except ValueError as e:
                    raise _errors.ConfigError(f'{section}: {option}: {e}', filepath=filepath)

    def _convert_to_client(self, options, option):
        client_name = options[option]
        if client_name not in aiobtclientapi.client_names():
            raise ValueError(f'{client_name}: Unknown client')
        return client_name

    def _convert_to_url(self, options, option):
        url = options[option]
        client_name = options['client']
        client_cls = getattr(aiobtclientapi, f'{client_name.capitalize()}API')
        try:
            return client_cls.URL(url)
        except ValueError as e:
            raise ValueError(f'{url}: {e}')

    _bool_values = {
        '1': True, 'yes': True, 'true': True, 'on': True,
        '0': False, 'no': False, 'false': False, 'off': False,
    }

    def _convert_to_bool(self, options, option):
        value = str(options[option]).lower()
        try:
            return self._bool_values[value]
        except KeyError:
            raise ValueError(f'{value}: Must be true/false, yes/no, on/off, 1/0')

    @property
    def filepath(self):
        """Where the configuration was read from"""
        return self._filepath

    @property
    def default(self):
        """First client config in the file"""
        section = next(iter(self._config))
        return self._config[section]

    def __getitem__(self, key):
        return self._config[key]

    def __len__(self):
        return len(self._config)

    def __iter__(self):
        return iter(self._config)

    def __repr__(self):
        return f'<{type(self).__name__} {self._filepath!r} {self._config!r}>'
