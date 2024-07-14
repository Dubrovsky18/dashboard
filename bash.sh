#!/bin/bash

cat <<EOT >> /etc/postgresql/16/main/conf.d/perf.conf
shared_buffers = 1GB
max_connections = 1024
effective_cache_size = 512MB

work_mem = 254MB
max_worker_processes = 4
max_parallel_workers = 4
max_parallel_maintenance_workers = 4
max_parallel_workers_per_gather = 4
maintenance_work_mem = 1GB

checkpoint_completion_target = 0.9
checkpoint_timeout = 20min
default_statistics_target = 300
random_page_cost = 1.0
effective_io_concurrency = 500
synchronous_commit = off
huge_pages = off
wal_buffers = 64MB
temp_buffers = 64MB
min_wal_size = 256MB
max_wal_size = 1GB
EOT
systemctl restart postgresql
