import argparse
import asyncio
import sys

from . import (__description__, __project_name__, __version__, _btclient,
               _config, _errors, _location)


def _parse_args(args):
    argparser = argparse.ArgumentParser(
        prog=__project_name__,
        description=__description__,
    )
    argparser.add_argument(
        'TORRENT',
        nargs='+',
        help='Path to torrent file',
    )
    argparser.add_argument(
        '--location', '-l',
        # TODO: Always use "extend" when Python 3.7 is no longer supported.
        #       https://docs.python.org/3/library/argparse.html#action
        action='extend' if sys.version_info >= (3, 8, 0) else 'append',
        nargs='+' if sys.version_info >= (3, 8, 0) else None,
        default=[],
        help=(
            'Potential download location of existing files in TORRENT '
            '(may be given multiple times)'
        ),
    )
    argparser.add_argument(
        '--locations-file', '--lf',
        default=_config.DEFAULT_LOCATIONS_FILEPATH,
        help='File containing newline-separated list of download locations',
    )
    argparser.add_argument(
        '--default', '-d',
        help='Default location if no existing files are found',
    )
    argparser.add_argument(
        '--clients-file', '--cf',
        default=_config.DEFAULT_CLIENTS_FILEPATH,
        help='File containing BitTorrent client connections',
    )
    argparser.add_argument(
        '--client', '-c',
        default=None,
        help='Add TORRENT to CLIENT (CLIENT is a section name in CLIENTS_FILE)',
    )
    argparser.add_argument(
        '--noclient', '-C',
        action='store_true',
        default=None,
        help='Do not add TORRENT to any client, print download location instead',
    )
    argparser.add_argument(
        '--version',
        action='version',
        version=f'{__project_name__} {__version__}',
    )
    argparser.add_argument(
        '--debug',
        nargs='?',
        metavar='FILE',
        help='Write debugging messages to FILE or STDERR if FILE is "-"',
    )
    return argparser.parse_args(args)


def _fatal_error(msg):
    sys.stderr.write(f'{msg}\n')
    sys.exit(1)


def _setup_debugging(args):
    # Debugging
    if args.debug == '-':
        import logging
        logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
    elif args.debug:
        import logging
        logging.basicConfig(filename=args.debug, level=logging.DEBUG)


def _get_locations(args):
    # Read locations file
    try:
        locations = _config.Locations(filepath=args.locations_file)
    except _errors.ConfigError as e:
        _fatal_error(str(e))
    else:
        # Prepend arguments from --location to locations from config file
        for location in args.location:
            if location in locations:
                locations.remove(location)
        locations[0:0] = args.location
        if not locations:
            _fatal_error(f'No locations specified. See: {__project_name__} --help')
        return locations


def _get_client_config(args):
    # Read client configurations from file
    try:
        configs = _config.Clients(filepath=args.clients_file)
    except _errors.ConfigError as e:
        _fatal_error(str(e))
    else:
        if args.client is not None:
            try:
                return configs[args.client]
            except KeyError:
                _fatal_error(f'Unknown client: {args.client}')
        elif configs:
            return configs.default


def _get_client(args):
    if not args.noclient:
        config = _get_client_config(args)
        if config:
            return _btclient.Client(config)


def _find_location(torrent, args):
    location_finder = _location.FindDownloadLocation(
        torrent=torrent,
        locations=_get_locations(args),
        default=args.default,
    )
    try:
        return location_finder.find()
    except _errors.FindError as e:
        _fatal_error(str(e))


async def _handle_location(location, torrent, client):
    if client:
        response = await client.add_torrent(torrent, location)
        for warning in response.warnings:
            sys.stderr.write(f'{torrent}: WARNING: {warning}\n')
        if response.errors:
            for error in response.errors:
                sys.stderr.write(f'{torrent}: {error}\n')
            return False  # Failure
        return True  # Success
    else:
        sys.stdout.write(f'{location}\n')
        return True  # Success


async def _cli(args):
    args = _parse_args(args)
    _setup_debugging(args)
    client = _get_client(args)

    exit_code = 0
    for torrent in args.TORRENT:
        location = _find_location(torrent, args)
        if not await _handle_location(location, torrent, client):
            exit_code = 1
    return exit_code


def cli():
    sys.exit(asyncio.run(_cli(sys.argv[1:])))
