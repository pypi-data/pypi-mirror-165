
****************
Customized style
****************

Styles in GooseMPL
==================

The following styles are part of *GooseMPL*:

*   ``goose``

    Customized layout settings.

*   ``goose-latex``

    Extend a style to enable the use of LaTeX,
    and change the font to LaTeX default Computer Modern font.

*   ``goose-tick-in``

    Place the tick-markers (*the little lines*)
    at the inside of the axes rather than at the outside.

*   ``goose-tick-lower``

    Shown only axes on the bottom and left side of the figure
    (those on the top and right are not shown).

See the :ref:`examples-pyplot`.

.. note::

    To install them::

        python -c "import GooseMPL; GooseMPL.copy_style()"

Background
==========

*matplotlib* has a very convenient way to customize plots while minimizing
the amount of customized code needed for this.
It employs easy-to-switch plotting styles with the same parameters as a ``matplotlibrc`` file.
The only thing needed to switch styles is:

.. code-block:: python

    import matplotlib.pyplot as plt
    plt.style.use('name_of_custom_style')

A number of styles are available. To list them use ``plt.style.available``.

Also, one can use one's own style.
This is a plain-text file ``name_of_custom_style.mplstyle`` stored in a
sub-directory ``stylelib`` of the *matplotlib* configuration directory; e.g.::

    ~/.matplotlib/stylelib/
    ~/.config/matplotlib/stylelib/

The exact directory depends on the operating system and the installation.
To find the directory to use on your system, use:

.. code-block:: python

    import matplotlib
    matplotlib.get_configdir()

.. note::

    More information in *matplotlib*'s
    `documentation <http://matplotlib.org/users/customizing.html>`__

Tips
====

Combining styles
----------------

Combining different styles is easily accomplished by including a list of styles. For example:

.. code-block:: python

    plt.style.use(['dark_background', 'presentation'])

Temporary styling
-----------------

To compose parts of the plot with a different style use:

.. code-block:: python

    with plt.style.context(('presentation')):
        plt.plot(np.sin(np.linspace(0, 2 * np.pi)))

Extending
---------

To get the available fields do the following:

.. code-block:: python

    import matplotlib as mpl

    print(mpl.rcParams)
