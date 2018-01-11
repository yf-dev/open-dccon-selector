#!/bin/bash
set -e

cd /frontend

if [ ! -z $1 ]
then
  exec $@
else
  yarn install
  exec yarn start
fi
