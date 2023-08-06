#!/bin/bash

rm -rf ../dist

(cd .. && rm -r ./**/**.pyc)

(cd .. && python setup.py sdist --formats=gztar)

(cd .. && twine upload dist/*)

