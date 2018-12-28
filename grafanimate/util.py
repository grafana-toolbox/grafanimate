#  -*- coding: utf-8 -*-
# (c) 2018 Andreas Motl <andreas@hiveeyes.org>
# License: GNU Affero General Public License, Version 3
import os
import sys
import socket
import logging
from contextlib import closing
from munch import munchify


def setup_logging(level=logging.INFO):
    log_format = '%(asctime)-15s [%(name)-30s] %(levelname)-7s: %(message)s'
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
