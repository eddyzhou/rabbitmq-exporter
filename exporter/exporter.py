#!/usr/bin/env python
# -*- coding: utf-8 -*-


from prometheus_client import Gauge

from .client import Api, Client


# ------- oeverview metrics -------
connections_total = Gauge('connections_total', 'Total number of open connections', ['node'])
channels_total = Gauge('channels_total', 'Total number of open channels', ['node'])
queues_total = Gauge('queues_total', 'Total number of queues in use', ['node'])
consumers_total = Gauge('consumers_total', 'Total number of consumers', ['node'])
exchanges_total = Gauge('exchanges_total', 'Total number of exchanges in use', ['node'])

# ------- nodes metrics -------
running = Gauge('running', 'Boolean for whether this node is up', ['node'])

fd_used = Gauge('fd_used', 'Used File descriptors', ['node'])
fd_limit = Gauge('fd_limit', 'File descriptors available', ['node'])

socket_used = Gauge('socket_used', 'File descriptors used as sockets.', ['node'])
socket_limit = Gauge('socket_limit', 'File descriptors available for use as sockets', ['node'])

mem_used = Gauge('mem_used', 'Memory used in bytes', ['node'])
mem_limit = Gauge('mem_limit', 'Point at which the memory alarm will go off', ['node'])
mem_alarm = Gauge('mem_alarm', 'Whether the memory alarm has gone off', ['node'])

disk_free = Gauge('disk_free', 'Disk free space in bytes', ['node'])
disk_free_alarm = Gauge('disk_free_alarm', 'Whether the disk alarm has gone off', ['node'])
disk_free_limit = Gauge('disk_free_limit', 'Point at which the disk alarm will go off', ['node'])

# ------- queues metrics -------
messages_total = Gauge('messages_total', 'Total number of messages in queue', ['queue'])


class Exporter(object):

    def __init__(self, host: str, auth: (str, str) = ('guest', 'guest')):
        self.client = Client(host, auth)

    def fetch_metrics(self):
        self.fetch_overview()
        self.fetch_nodes()
        self.fetch_queues()

    def fetch_overview(self):
        data = self.client.fetch(Api.overview)
        node = data['node']
        object_totals = data['object_totals']
        connections_total.labels(node).set(object_totals['connections'])
        channels_total.labels(node).set(object_totals['channels'])
        queues_total.labels(node).set(object_totals['queues'])
        consumers_total.labels(node).set(object_totals['consumers'])
        exchanges_total.labels(node).set(object_totals['exchanges'])

    def fetch_queues(self):
        data = self.client.fetch(Api.queues)
        for queue in data:
            name = queue['name']
            # messages = queue['messages']
            messages = queue['backing_queue_status']['len']
            messages_total.labels(name).set(messages)

    def fetch_nodes(self):
        data = self.client.fetch(Api.nodes)
        for node in data:
            name = node['name']
            is_running = node['running']
            if not is_running:
                running.labels(name).set(0)
            else:
                running.labels(name).set(1)
                self._build_node_metrics(node)

    def _build_node_metrics(self, node: dict):
        name = node['name']
        fd_used.labels(name).set(node['fd_used'])
        fd_limit.labels(name).set(node['fd_total'])
        socket_used.labels(name).set(node['sockets_used'])
        socket_limit.labels(name).set(node['sockets_total'])
        mem_used.labels(name).set(node['mem_used'])
        mem_limit.labels(name).set(node['mem_limit'])
        mem_alarm.labels(name).set(1 if node['mem_alarm'] else 0)
        disk_free.labels(name).set(node['disk_free'])
        disk_free_limit.labels(name).set(node['disk_free_limit'])
        disk_free_alarm.labels(name).set(1 if node['disk_free_alarm'] else 0)
