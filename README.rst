========
refparse
========

utterly default so far


.. image:: https://img.shields.io/pypi/v/refparse.svg
        :target: https://pypi.python.org/pypi/refparse

.. image:: https://img.shields.io/travis/MattWellie/refparse.svg
        :target: https://travis-ci.com/MattWellie/refparse

.. image:: https://readthedocs.org/projects/refparse/badge/?version=latest
        :target: https://refparse.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status




Generates typeset documents from genomic reference sequences


* Free software: MIT license
* Documentation: https://refparse.readthedocs.io


Features
--------

* Add files to the input

Usage
-------

Build the docker image using

``docker build -t refparse:local``

This can then be run by mounting the input and output directories:

``docker run -v ${PWD}/input:/input -v ${PWD}/output:/output refparse:local -i input/LRG_TEST.xml``

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
