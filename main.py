#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer

from exporter.exporter import Exporter

from prometheus_client import core, generate_latest


def make_metrics_handler(exporter: Exporter) -> BaseHTTPRequestHandler:
    class MetricsHandler(BaseHTTPRequestHandler):
        exporter = exporter

        def do_GET(self):
            exporter.fetch_metrics()
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain; version=0.0.4; charset=utf-8')
            self.end_headers()
            self.wfile.write(generate_latest(core.REGISTRY))

        def log_message(self, format, *args):
            return

    return MetricsHandler


def start_http_server(exporter: Exporter, port: int, addr: str=''):
    httpd = HTTPServer((addr, port), make_metrics_handler(exporter))
    httpd.serve_forever()


if __name__ == '__main__':
    if len(sys.argv) < 3:
        sys.exit('Usage: python mq_host listen_port <addr>')
    else:
        mq_host = sys.argv[1]
        port = int(sys.argv[2])
        addr = sys.argv[3] if len(sys.argv) >= 4 else '0.0.0.0'

        exporter = Exporter(mq_host)
        start_http_server(exporter, port, addr)
