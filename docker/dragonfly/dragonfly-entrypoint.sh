#!/bin/sh

# This is important in order to provide enough locked memory to dragonfly
# when running on kernels < 5.12.
# This line should reside before `set -e` so it could fail silently
# in case the container runs in non-privileged mode.
ulimit -l 65000 2> /dev/null

set -e

dragonfly \
  --logtostderr \
  --save_schedule=$REDIS_BACKUP_DB \
  --dir=/data \
  --dbfilename=$REDIS_DATABASE \
  --requirepass=$REDIS_PASSWORD