ParamsDict
----------

.. image:: https://badge.fury.io/py/paramsdict.svg
    :target: https://badge.fury.io/py/paramsdict

.. image:: https://badgen.net/badge//gh/paramsdict?icon=github
    :target: https://github.com/adamoppenheimer/paramsdict

``ParamsDict`` is a Python package for defining user-friendly parameter dictionaries.

It has three advantages over built-in dictionaries:

1. Keys are fixed. This prevents users from accidentally mistyping keys - in particular, a mistyped key in a built-in dictionary will not raise an error, and the user may not have a way to know there is a mistake in their code.
2. Values can be constrained. This guarantees users enter valid parameters.
3. All keys have linked descriptions. This means users can check parameter definitions without having to refer to the documentation.

The package also generates clear errors messages so if an input is an invalid, the user knows why it didn't work.

``ParamsDict`` is used in `BipartitePandas <https://github.com/tlamadon/bipartitepandas/>`_ and `PyTwoWay <https://github.com/tlamadon/pytwoway/>`_. The original code was written for those projects, under the supervision of Professor Thibaut Lamadon at the University of Chicago. The package was inspired by `this <https://stackoverflow.com/a/14816620/17333120/>`_ post on Stack Overflow.

Installation
------------

The package provides a Python interface. Installation is handled by ``pip``. The source of the package is available on GitHub at `ParamsDict <https://github.com/adamoppenheimer/paramsdict>`_.

To install via pip, from the command line run::

    pip install paramsdict

To make sure you are running the most up-to-date version of ``ParamsDict``, from the command line run::

    pip install --upgrade paramsdict

Quick Start
-----------

Say you are writing a function that simulates values from a normal distribution and you want the user to be able to specify the number of draws, as well as the mean and standard deviation of the normal distribution. You also want to constrain the user so that the number of draws is a positive integer, while the mean and standard deviation must be floats or integers and the standard deviation is non-negative. Finally, assume you have two algorithms for simulating from the normal distribution, ``'a'`` and ``'b'``, which you want the user to be able to specify.

.. code-block:: python

    from paramsdict import ParamsDict

    def _gt0(x):
        return x > 0
    def _gteq0(x):
        return x >= 0

    sim_params = ParamsDict({
        'n': (10, 'type_constrained', (int, _gt0),
            '''
                (default=10) Number of draws to simulate.
            ''', '> 0'),
        'mean': (0, 'type', (int, float),
            '''
                (default=0) Mean of draws.
            ''', None),
        'sd': (1, 'type_constrained', ((int, float), _gteq0),
            '''
                (default=1) sd of draws.
            ''', '>= 0'),
        'algorithm': ('a', 'set', ['a', 'b'],
            '''
                (default='a') Algorithm for simulating from normal distribution.
            ''', None)
    })

Now the user can instantiate a new instance of ``sim_params`` by running ``my_sim_params = sim_params()``.

They can set their own values by inputting a dictionary while instantiating the ``ParamsDict``, e.g. ``my_sim_params = sim_params({'sd': 2})``. If they enter an invalid value, it will raise an error.

If the user wants to know what a particular key does, they can run ``sim_params().describe(key)``, e.g. if they run ``sim_params().describe('sd')`` it will print a description of ``'sd'``. Alternatively, to print descriptions for every key in the parameter dictionary, they can run ``sim_params().describe_all()``.

Advanced
--------

``ParamsDict`` includes a variety of options for parameters. These include:

- ``'type'`` - the key must be associated with a particular type
- ``'list_of_type'`` - the value must be a particular type or a list of values of a particular type
- ``'type_none'`` - the value can either be None or must be a particular type
- ``'list_of_type_none'``: the value can either be None or must be a particular type or a list of values of a particular type
- ``'type_constrained'`` - the value must be a particular type and fulfill given constraints
- ``'type_constrained_none'`` - the value can either be None or must be a particular type and fulfill given constraints
- ``'dict_of_type'`` - the value must be a dictionary where the values are of a particular type
- ``'dict_of_type_none'`` - the value can either be None or must be a dictionary where the values are of a particular type
- ``'array_of_type'`` - the value must be an array of values of a particular datatype
- ``'array_of_type_none'`` - the value can either be None or must be an array of values of a particular datatype
- ``'array_of_type_constrained'`` - the value must be an array of values of a particular datatype and fulfill given constraints
- ``'array_of_type_constrained_none'`` - the value can either be None or must be an array of values of a particular datatype and fulfill given constraints
- ``'set'`` - the value must be a member of a given set of values
- ``'list_of_set'`` - the value must be a member of a given set of values or a list of members of a given set of values
- ``'any'`` - the value can be anything

Author
------

Adam A. Oppenheimer,
Graduate Student, University of Minnesota - Twin Cities,
oppen040@umn.edu
