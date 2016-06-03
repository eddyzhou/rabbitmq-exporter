#!/usr/bin/env python
# -*- coding: utf-8 -*-

from enum import Enum
from typing import TypeVar

import requests


class Api(Enum):
    overview = 1
    nodes = 2
    queues = 3

T = TypeVar('T', dict, list)

class Client(object):

    def __init__(self, mq_url: str, auth: (str, str) = ('guest', 'guest')):
        if not mq_url.startswith('http'):
            mq_url = 'http://' + mq_url
        self.mq_url = mq_url
        self.auth = auth

    def fetch(self, api: Api) -> T:
        url = self.mq_url.rstrip('/') + '/api/' + api.name
        r = requests.get(url, auth=self.auth, timeout=3)
        assert r.status_code == requests.codes.ok
        return r.json()


if __name__ == '__main__':
    c = Client('10.10.28.2:15672')
    print('overview:', c.fetch(Api.overview))
    print('nodes:', c.fetch(Api.nodes))
    print('queues:', c.fetch(Api.queues))
