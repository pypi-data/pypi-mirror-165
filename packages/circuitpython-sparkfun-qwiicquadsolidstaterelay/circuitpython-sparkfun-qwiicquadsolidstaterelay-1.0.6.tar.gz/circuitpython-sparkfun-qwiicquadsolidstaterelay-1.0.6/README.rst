Introduction
============


.. image:: https://readthedocs.org/projects/circuitpython-sparkfun-qwiicquadsolidstaterelay/badge/?version=latest
    :target: https://circuitpython-sparkfun-qwiicquadsolidstaterelay.readthedocs.io/
    :alt: Documentation Status

.. image:: https://img.shields.io/discord/327254708534116352.svg
    :target: https://adafru.it/discord
    :alt: Discord

.. image:: https://github.com/gbeland/CircuitPython_Sparkfun_QwiicQuadSolidStateRelay/workflows/Build%20CI/badge.svg
    :target: https://github.com/gbeland/CircuitPython_Sparkfun_QwiicQuadSolidStateRelay/actions
    :alt: Build Status

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black
    :alt: Code Style: Black

CircuitPython library for SparkFun Qwiic Quad Solid State Relay Kit (COM-16833).

.. image:: https://cdn.sparkfun.com//assets/parts/1/5/7/5/4/16833-SparkFun_Qwiic_Quad_Solid_State_Relay_Kit-12.jpg
    :target: https://www.sparkfun.com/products/16833
    :alt: SparkFun Qwiic Quad Solid State Relay Kit (COM-16833)

`SparkFun Qwiic Quad Solid State Relay Kit (COM-16566) <https://www.sparkfun.com/products/16833>`_

Dependencies
=============
This driver depends on:

* `Adafruit CircuitPython <https://github.com/adafruit/circuitpython>`_
* `Bus Device <https://github.com/adafruit/Adafruit_CircuitPython_BusDevice>`_
* `SparkFun Qwiic Quad Solid State Relay Kit (COM-16566) Hardware <https://www.sparkfun.com/products/16833>`_

Please ensure all dependencies are available on the CircuitPython filesystem.
This is easily achieved by downloading
`the Adafruit library and driver bundle <https://circuitpython.org/libraries>`_
or individual libraries can be installed using
`circup <https://github.com/adafruit/circup>`_.

Installing from PyPI
=====================
.. note:: This library is not available on PyPI yet. Install documentation is included
   as a standard element. Stay tuned for PyPI availability!

On supported GNU/Linux systems like the Raspberry Pi, you can install the driver locally `from
PyPI <https://pypi.org/project/circuitpython-sparkfun-qwiicquadsolidstaterelay/>`_.
To install for current user:

.. code-block:: shell

    pip3 install circuitpython-sparkfun-qwiicquadsolidstaterelay

To install system-wide (this may be required in some cases):

.. code-block:: shell

    sudo pip3 install circuitpython-sparkfun-qwiicquadsolidstaterelay

To install in a virtual environment in your current project:

.. code-block:: shell

    mkdir project-name && cd project-name
    python3 -m venv .env
    source .env/bin/activate
    pip3 install circuitpython-sparkfun-qwiicquadsolidstaterelay



Installing to a Connected CircuitPython Device with Circup
==========================================================

Make sure that you have ``circup`` installed in your Python environment.
Install it with the following command if necessary:

.. code-block:: shell

    pip3 install circup

With ``circup`` installed and your CircuitPython device connected use the
following command to install:

.. code-block:: shell

    circup install sparkfun_qwiicquadsolidstaterelay

Or the following command to update an existing version:

.. code-block:: shell

    circup update

Usage Example
=============
.. code-block::

    """ QuadRelayTest """
    # QuadRelayTest: Copyright (c) 2022 Graham Beland
    #
    # SPDX-License-Identifier: MIT
    # import the CircuitPython board and busio libraries
    import time as tm
    # CircuitPython board
    import board
    # the sparkfun_qwiicquadsolidstaterelay
    import sparkfun_qwiicquadsolidstaterelay

    # Create bus object using the board's I2C port
    i2c = board.I2C()

    # Note: default i2c address is 8
    theRelay = sparkfun_qwiicquadsolidstaterelay.Sparkfun_QwiicQuadSolidStateRelay(i2c)
    print("Opened: Relay Controller")
    if theRelay.connected:
        print("Relay connected. ")
        theRelay.relay_on(1)
        tm.sleep(1)
        theRelay.relay_off(1)
    else:
        print("Relay does not appear to be connected. Please check wiring.")


Documentation
=============
API documentation for this library can be found on `Read the Docs <https://circuitpython-sparkfun-qwiicquadsolidstaterelay.readthedocs.io/>`_.

For information on building library documentation, please check out
`this guide <https://learn.adafruit.com/creating-and-sharing-a-circuitpython-library/sharing-our-docs-on-readthedocs#sphinx-5-1>`_.

Contributing
============

Contributions are welcome! Please read our `Code of Conduct
<https://github.com/gbeland/CircuitPython_Sparkfun_QwiicQuadSolidStateRelay/blob/HEAD/CODE_OF_CONDUCT.md>`_
before contributing to help this project stay welcoming.
