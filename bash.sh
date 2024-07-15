#!/bin/bash

cat <<EOT >> /etc/postgresql/16/main/conf.d/perf.conf
shared_buffers = 256MB
max_connections = 100
effective_cache_size = 256MB

work_mem = 256MB
max_worker_processes = 4
max_parallel_workers = 4
max_parallel_maintenance_workers = 4
max_parallel_workers_per_gather = 4

checkpoint_completion_target = 0.9
checkpoint_timeout = 20min
default_statistics_target = 300
random_page_cost = 1.0
effective_io_concurrency = 300
synchronous_commit = off
huge_pages = off
EOT
systemctl restart postgresql
