#!/bin/sh
source=$(cat $1)
echo "$source" | node topy.js > tmp.py
