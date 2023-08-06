
# To execute tests:<a id="sec-1" name="sec-1"></a>

    $ cd dameformats
    $ ./runtests.sh
    $ nosetests3 tests

# Pypi<a id="sec-2" name="sec-2"></a>

-   To install from local:

    $ pip install -e .

-   To install create tar.gz in dist directory:

    $ python3 setup.py register sdist

-   To upload to pypi:

    $ twine upload dist/dameformats-0.1.tar.gz

-   You can install from Internet in a python virtual environment to check:

    $ python3 -m venv /tmp/funny
    $ cd /tmp/funny
    $ source bin/activate
    $ pip3 install dameformats