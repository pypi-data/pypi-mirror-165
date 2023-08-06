# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['belay', 'belay.cli', 'belay.snippets']

package_data = \
{'': ['*']}

install_requires = \
['pyserial>=3.1,<4.0', 'typer[all]>=0.6,<0.7']

entry_points = \
{'console_scripts': ['belay = belay.cli.main:app']}

setup_kwargs = {
    'name': 'belay',
    'version': '0.6.0',
    'description': '',
    'long_description': '.. image:: https://raw.githubusercontent.com/BrianPugh/belay/main/assets/logo_white_400w.png\n\n|Python compat| |PyPi| |GHA tests| |readthedocs|\n\n\nBelay\n=====\n\n.. inclusion-marker-do-not-remove\n\nBelay is a library that enables the rapid development of projects that interact with hardware via a MicroPython or CircuitPython compatible board.\n\nBelay works by interacting with the REPL interface of a MicroPython board from Python code running on PC.\n\nBelay supports wired serial connections (USB) and wireless connections via WebREPL over WiFi.\n\n`Quick Video of Belay in 22 seconds.`_\n\nSee `the documentation`_ for usage and other details.\n\nWho is Belay For?\n=================\n\nBelay is for people creating a software project that needs to interact with hardware.\nExamples include:\n\n* Control a motor so a webcam is always pointing at a person.\n\n* Turn on an LED when you receive a notification.\n\n* Read a potentiometer to control system volume.\n\nIf you have no need to run Python code on PC, then Belay is not for you.\n\n\nWhat Problems Does Belay Solve?\n===============================\n\nTypically, having a python script interact with hardware involves 3 major challenges:\n\n1. On-device firmware (usually C or MicroPython) for directly handling hardware interactions. Typically this is developed, compiled, and uploaded as a (nearly) independent project.\n\n2. A program on your computer that performs the tasks specified and interacts with the device.\n\n3. Computer-to-device communication protocol. How are commands and results transferred? How does the device execute those commands?\n\n\nThis is lot of work if you just want your computer to do something simple like turn on an LED.\nBelay simplifies all of this by merging steps 1 and 2 into the same codebase, and manages step 3 for you.\nCode is automatically synced at the beginning of script execution.\n\nInstallation\n============\n\nBelay requires Python ``>=3.8`` and can be installed via:\n\n.. code-block:: bash\n\n   pip install belay\n\nThe MicroPython-compatible board only needs MicroPython installed; no additional preparation is required.\nIf using CircuitPython, and additional modification needs to be made to ``boot.py``. See `documentation <https://belay.readthedocs.io/en/latest/CircuitPython.html>`_ for details.\n\nExamples\n========\n\nTurning on an LED with Belay takes only 6 lines of code.\nFunctions decorated with the ``task`` decorator are sent to the device and interpreted by the MicroPython interpreter.\nCalling the decorated function on-host sends a command to the device to execute the actual function.\n\n.. code-block:: python\n\n   import belay\n\n   device = belay.Device("/dev/ttyUSB0")\n\n\n   @device.task\n   def set_led(state):\n       print(f"Printing from device; turning LED to {state}.")\n       Pin(25, Pin.OUT).value(state)\n\n\n   set_led(True)\n\nOutputs from ``print`` calls from on-device user-code are forwarded to host ``stdout``.\n\n`For more examples, see the examples folder.`_\n\n\n.. |GHA tests| image:: https://github.com/BrianPugh/belay/workflows/tests/badge.svg\n   :target: https://github.com/BrianPugh/belay/actions?query=workflow%3Atests\n   :alt: GHA Status\n.. |Codecov report| image:: https://codecov.io/github/BrianPugh/belay/coverage.svg?branch=main\n   :target: https://codecov.io/github/BrianPugh/belay?branch=main\n   :alt: Coverage\n.. |readthedocs| image:: https://readthedocs.org/projects/belay/badge/?version=latest\n        :target: https://belay.readthedocs.io/en/latest/?badge=latest\n        :alt: Documentation Status\n.. |Python compat| image:: https://img.shields.io/badge/>=python-3.8-blue.svg\n.. |PyPi| image:: https://img.shields.io/pypi/v/belay.svg\n        :target: https://pypi.python.org/pypi/belay\n.. _Quick Video of Belay in 22 seconds.: https://www.youtube.com/watch?v=wq3cyjSE8ek\n.. _the documentation: https://belay.readthedocs.io\n.. _For more examples, see the examples folder.:  https://github.com/BrianPugh/belay/tree/main/examples\n',
    'author': 'Brian Pugh',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/BrianPugh/belay',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
