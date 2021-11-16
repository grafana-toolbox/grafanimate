#  -*- coding: utf-8 -*-
# (c) 2018 Andreas Motl <andreas@hiveeyes.org>
# License: GNU Affero General Public License, Version 3
import re
import os
import sys
import socket
import logging
from pathlib import Path

from munch import munchify
from contextlib import closing
from unidecode import unidecode


def setup_logging(level=logging.INFO):
    log_format = '%(asctime)-10s [%(name)-30s] %(levelname)-7s: %(message)s'
    logging.basicConfig(
        format=log_format,
        stream=sys.stderr,
        level=level)

    # TODO: Control debug logging of HTTP requests through yet another commandline option "--debug-http" or "--debug-requests"
    requests_log = logging.getLogger('requests')
    requests_log.setLevel(logging.WARN)


def normalize_options(options, lists=None):
    lists = lists or []
    normalized = {}
    for key, value in options.items():
        key = key.strip('--<>')
        normalized[key] = value
    for key in lists:
        normalized[key] = read_list(normalized[key])
    return munchify(normalized)


def read_list(data, separator=u','):
    if data is None:
        return []
    result = list(map(lambda x: x.strip(), data.split(separator)))
    if len(result) == 1 and not result[0]:
        result = []
    return result


def find_program_candidate(candidates):
    for candidate in candidates:
        if os.path.isfile(candidate):
            return candidate


def check_socket(host, port):
    # https://stackoverflow.com/questions/19196105/python-how-to-check-if-a-network-port-is-open-on-linux
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
        sock.settimeout(1)
        if sock.connect_ex((host, port)) == 0:
            return True
        else:
            return False


def format_date_human(date, interval=None):
    #pattern = '%Y-%m-%d'
    pattern = '%Y-%m-%dT%H-%M-%S'
    #if interval in ['secondly', 'minutely', 'hourly']:
    #    pattern = '%Y-%m-%dT%H-%M-%S'
    date_formatted = date.strftime(pattern)
    return date_formatted


def format_date_grafana(date, interval=None):
    pattern = '%Y-%m-%d'
    if interval in ['secondly', 'minutely', 'hourly'] or interval.endswith('min'):
        pattern = '%Y-%m-%dT%H:%M:%S'
    date_formatted = date.strftime(pattern)
    return date_formatted


def filter_dict(data, keys):
    return {k: v for k, v in data.items() if k in keys}


def slug(text):
    """Make a URL-safe, human-readable version of the given text

    This will do the following:

    1. decode unicode characters into ASCII
    2. shift everything to lowercase
    3. strip whitespace
    4. replace other non-word characters with dashes
    5. strip extra dashes

    This somewhat duplicates the :func:`Google.slugify` function but
    slugify is not as generic as this one, which can be reused
    elsewhere.

    Stolen from beetsplug.lyrics.
    """
    return re.sub(r'\W+', '-', unidecode(text).lower().strip()).strip('-')


def ensure_directory(path):
    directory = os.path.dirname(path)
    if not os.path.exists(directory):
        os.makedirs(directory)


def asbool(obj):
    # from sqlalchemy.util.asbool
    if isinstance(obj, str):
        obj = obj.strip().lower()
        if obj in ["true", "yes", "on", "y", "t", "1"]:
            return True
        elif obj in ["false", "no", "off", "n", "f", "0"]:
            return False
        else:
            raise ValueError("String is not true/false: %r" % obj)
    return bool(obj)


def is_sequence(seq):
    # From `numpy.distutils.misc_util`
    if isinstance(seq, str):
        return False
    try:
        len(seq)
    except Exception:
        return False
    return True


def as_list(seq):
    # From `numpy.distutils.misc_util`
    if is_sequence(seq):
        return list(seq)
    else:
        return [seq]


def import_module(name: str, path: str):
    """
    Import Python module from file.
    """

    # Use absolute path.
    modulefile = Path(path).absolute()

    # Import module.
    # https://stackoverflow.com/a/67692
    import importlib.util

    spec = importlib.util.spec_from_file_location(name, modulefile)
    if spec is None:
        raise FileNotFoundError(f"Unable to find module file {modulefile}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    return mod
