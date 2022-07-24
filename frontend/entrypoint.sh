#!/bin/sh
set -e

cd /frontend

if [ ! -z $1 ]
then
  exec $@
else
  yarn
  exec yarn build
fi
