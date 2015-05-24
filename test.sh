#!/bin/sh

NOSEBIN="env/bin/nosetests"
if [ ! -f "$NOSEBIN" ]; then
  NOSEBIN=nosetests
fi

$NOSEBIN --verbose --rednose --with-coverage --cover-package=jsonserver --cover-erase
