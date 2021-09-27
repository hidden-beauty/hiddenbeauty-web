#!/usr/bin/env python3

import datetime
import os
import sys

DAYS_TO_KEEP_LOGS = 7

def remove_old_logs(log_dir):

    for dir in sorted(os.listdir(log_dir)):
        if dir in ['.', '..']:
            continue

        try:
            _, _, date, _ = dir.split(".")
        except ValueError:
            continue

        dt = datetime.datetime.strptime(date, '%Y-%m-%d')
        days_old = (datetime.datetime.now() - dt).days
        print("%s %d days old" % (dir, days_old), end='')
        if days_old >= DAYS_TO_KEEP_LOGS:
            rmlog = os.path.join(log_dir, dir)
            print(", removed.", end='')
            os.unlink(rmlog)

        print()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("%s <log_dir>" % sys.argv[0])
        sys.exit(-1)

    remove_old_logs(sys.argv[1])
