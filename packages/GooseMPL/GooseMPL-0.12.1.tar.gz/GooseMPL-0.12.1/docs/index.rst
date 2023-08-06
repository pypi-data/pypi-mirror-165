
********
GooseMPL
********

*GooseMPL* provides a style and several style extensions for *matplotlib*,
some custom functions that extend *matplotlib*,
and several examples to make professional plots using *matplotlib*.

To obtain *GooseMPL* one can do one of the following:

1.  Using Conda::

        conda install -c conda-forge goosempl

2.  Using PyPi::

        python -m pip install GooseMPL

3.  Manual installation.
    After `downloading <https://github.com/tdegeus/GooseMPL/zipball/master>`_
    navigate to the downloaded folder than run::

        python -m pip install .

Then install the *matplotlib* style files using::

    python -c "import GooseMPL; GooseMPL.copy_style()"

You'll only have to do this once after installing/updating.

.. note::

    This library is free to use under the
    `MIT license <https://github.com/tdegeus/GooseMPL/blob/master/LICENSE>`_.
    Any additions are very much appreciated, in terms of suggested functionality, code,
    documentation, testimonials, word of mouth advertisement, ....
    Bug reports or feature requests can be filed on
    `GitHub <http://github.com/tdegeus/GooseMPL>`_.
    As always, the code comes with no guarantee.
    None of the developers can be held responsible for possible mistakes.

    Download:
    `.zip file <https://github.com/tdegeus/GooseMPL/zipball/master>`_ |
    `.tar.gz file <https://github.com/tdegeus/GooseMPL/tarball/master>`_.

    (c - `MIT <https://github.com/tdegeus/GooseMPL/blob/master/LICENSE>`_)
    T.W.J. de Geus (Tom) | tom@geus.me | `www.geus.me <http://www.geus.me>`_ |
    `github.com/tdegeus/GooseMPL <http://github.com/tdegeus/GooseMPL>`_

Contents
========

.. toctree::
    :maxdepth: 2

    style.rst
    goosempl.rst
    examples/pyplot/readme.rst
    examples/goosempl/readme.rst
    tips.rst

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
