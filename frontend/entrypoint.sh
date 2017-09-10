#!/bin/bash
set -e

cd /frontend

if [ ! -z $1 ]
then
  exec yarn $@
else
  yarn install
  exec yarn start
fi
