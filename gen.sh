#!/usr/bin/env bash

file="./$(date +'%Y-%m-%d').log.md"
touch $file
echo "# $(date +'%A, %B %d, %Y %I:%M %p')" >> $file
