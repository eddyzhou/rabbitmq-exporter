# RabbitMQ Exporter

Prometheus exporter for RabbitMQ metrics, based on RabbitMQ HTTP API.

### Dependencies

Python3.5+

### Metrics

Total number of:

* channels
* connections
* consumers
* exchanges
* queues
* fd_used
* fd_limit
* socket_used
* socket_limit
* mem_used
* mem_limit
* disk_free
* disk_free_limit
* messages

### Usage

python mq_host listen_port <addr>

