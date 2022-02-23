#!/usr/bin/env bash

if [ $1 == "repo" ]
then
  python3 ./byrepo.py $1 $2
elif [ $1 == "date" ]
then
  python3 ./bydate.py $1
elif [ $1 == "range" ]
then
  python3 ./byrange.py
else
  echo "invalid command"
  echo "usage: ./gen.sh <repo | date | range> [date (YYYY-MM-DD)] [repo]"
fi
