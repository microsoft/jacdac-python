#!/bin/sh

test -f jacdac/__init__.py || exit 1
tar -cf - * | ssh pi@192.168.0.129 'cd ~/jacdac-python && tar -xf - && echo "start" && gpioinfo && python3 -u -m examples.blinky'
