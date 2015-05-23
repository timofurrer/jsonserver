#!/bin/sh

env/bin/nosetests --verbose --rednose --with-coverage --cover-package=jsonserver --cover-erase
