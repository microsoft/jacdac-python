#!/bin/sh

test -f jacdac/__init__.py || exit 1
tar -cf - * | ssh pi 'cd ~/jacdac-python && tar -xf - && echo "start" && python3 -u -m jacdac.real_time_clock.test'
