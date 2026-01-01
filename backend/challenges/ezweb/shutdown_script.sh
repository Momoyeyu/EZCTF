#!/bin/sh

# 脚本执行周期（这里是每两小时执行一次）
CRON_SCHEDULE="0 */2 * * *"

echo "$CRON_SCHEDULE /bin/sh /shutdown_containers.sh" > /etc/crontabs/root
crond -f
