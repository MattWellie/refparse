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

* Add files to the input folder (examples are already present)
* Expect output in the output folder

Preferred Usage
-------

This code is designed to be run using a chain of Docker images... That's really the only reason I've revisited this code.

You will need a local docker desktop to be running

This is facilitated through the make file, run ``make`` to see options

Example:
    $ make pdf target_file=input/LRG_110.xml

This will typeset the file input/LRG_110.xml into a PDF, and write the output into ./output/pdf


Manual Usage
-------

Build the docker image using

``docker build -t refparse:local .``

This can then be run by mounting the input and output directories:

``docker run -v ${PWD}/input:/input -v ${PWD}/output:/output refparse:local -i input/LRG_TEST.xml``

to run the resulting tex file into a pdf:
docker run --rm --user $UID:$GID -v $PWD:/sources embix/pdflatex:v1 output/output_file.tex

There is no local installation of pdflatex because it is huge and gross
The embix image is sufficient and stable
Because it is huge, gross, and optional the images are kept separate


Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
