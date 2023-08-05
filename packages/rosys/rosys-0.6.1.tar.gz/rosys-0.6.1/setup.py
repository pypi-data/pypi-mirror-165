# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rosys',
 'rosys.automation',
 'rosys.debugging',
 'rosys.debugging.legacy',
 'rosys.driving',
 'rosys.geometry',
 'rosys.hardware',
 'rosys.hardware.communication',
 'rosys.pathplanning',
 'rosys.test',
 'rosys.timelapse',
 'rosys.vision']

package_data = \
{'': ['*']}

install_requires = \
['aenum>=3.1.5,<4.0.0',
 'aiocache>=0.11.1,<0.12.0',
 'aiohttp>=3.7.4,<4.0.0',
 'aioserial>=1.3.0,<2.0.0',
 'asyncio>=3.4.3,<4.0.0',
 'coloredlogs>=15.0.1,<16.0.0',
 'dataclasses-json>=0.5.7,<0.6.0',
 'humanize>=4.0.0,<5.0.0',
 'more-itertools>=8.10.0,<9.0.0',
 'msgpack>=1.0.3,<2.0.0',
 'networkx>=2.6.2,<3.0.0',
 'nicegui>=0.8.4',
 'numpy>=1.20.1,<2.0.0',
 'objgraph>=3.5.0,<4.0.0',
 'opencv-contrib-python-headless>=4.5.4,<5.0.0',
 'opencv-python>=4.5.5,<5.0.0',
 'psutil>=5.9.0,<6.0.0',
 'pyloot>=0.0.7,<0.0.8',
 'pyserial>=3.5,<4.0',
 'python-socketio[asyncio_client]>=5.3.0,<6.0.0',
 'requests>=2.25.1,<3.0.0',
 'retry>=0.9.2,<0.10.0',
 'scipy>=1.7.2,<2.0.0',
 'sh>=1.14.2,<2.0.0',
 'simplejson>=3.17.2,<4.0.0',
 'tabulate>=0.8.9,<0.9.0',
 'ujson==5.4.0',
 'uvloop>=0.16.0,<0.17.0',
 'yappi>=1.3.3,<2.0.0']

setup_kwargs = {
    'name': 'rosys',
    'version': '0.6.1',
    'description': 'Modular Robot System With Elegant Automation Capabilities',
    'long_description': '# RoSys - The Robot System\n\nRoSys provides an easy-to-use robot system.\nIts purpose is similar to [ROS](https://www.ros.org/).\nBut RoSys is fully based on modern web technologies and focusses on mobile robotics.\n\nSee full documentation at [rosys.io](https://rosys.io/).\n\nCurrently RoSys is mostly tested and developed on the [Zauberzeug Robot Brain](https://www.zauberzeug.com/robot-brain.html) which uses [Lizard](https://lizard.dev/) for communication with motors, sensors and other peripherals.\nBut the software architecture of RoSys also allows you to write your own modules if you prefer another industrial PC or setup.\n\n## Principles\n\n### All Python\n\nBusiness logic is wired in Python while computation-heavy tasks are encapsulated through websockets or bindings.\n\n### Shared State\n\nAll code can access and manipulate a shared and typesafe state -- this does not mean it should.\nGood software design is still necessary.\nBut it is much easier to do if you do not have to perform serialization all the time.\n\n### No Threading\n\nThanks to [asyncio](https://docs.python.org/3/library/asyncio.html) you can write the business logic without locks and mutex mechanisms.\nThe running system feels like everything is happening in parallel.\nBut each code block is executed one after another through an event queue and yields execution as soon as it waits for I/O or heavy computation.\nThe latter is still executed in threads to not block the rest of the business logic.\n\n### Web UI\n\nMost machines need some kind of human interaction.\nWe made sure your robot can be operated fully off the grid with any web browser by incorporating [NiceGUI](https://nicegui.io/).\nIt is also possible to proxy the user interface through a gateway for remote operation.\n\n### Simulation\n\nRobot hardware is often slower than your own computer.\nTherefore RoSys supports a simulation mode for rapid development.\nTo get maximum performance the current implementation does not run a full physics engine.\n\n### Testing\n\nYou can use [pytest](https://docs.pytest.org/) to write high-level integration tests.\nIt is based on the above-described simulation mode and accelerates the robot\'s time for super fast execution.\n\n## Architecture and Features\n\n### Modules\n\nRoSys modules basically are Python modules encapsulate certain functionality.\nThey can hold their own state, register lifecycle hooks, run methods repeatedly and subscribe to or raise [events](#events).\nMost modules depend on other modules.\n\n### Lifecycle Hooks And Loops\n\nModules can register functions for being called `on_startup` or `on_shutdown` as well as repeatedly with a given interval.\n\n### Events\n\nModules can provide events to allow coupling otherwise separated modules of the system.\nFor example on module might read sensor data and raise an event `NEW_SENSOR_DATA`, without knowing of any consumers.\nAnother module can register on `NEW_SENSOR_DATA` and act accordingly when being called.\n\n### Automations\n\nRoSys provides an `Automator` module for running "automations".\nAutomations are coroutines that can not only be started and stopped, but also paused and resumed, e.g. using `AutomationControls`.\n\n### Persistence\n\nModules can register backup and restore methods to read and write their state to disk.\n\n### RoSys Time\n\nIf you want to delay the execution, you should invoke `await rosys.sleep(seconds: float)`.\nThis causes to wait until the _RoSys time_ has elapsed the desired amount of time.\nIn pytests the RoSys time is simulated and can advance much faster if no CPU-intensive operation is performed.\n\n### Threading And Multiprocessing\n\nNot every piece of code is already using asyncio.\nThe actor class provides convenience functions for IO and CPU bound work.\n\nIO Bound:\nIf you need to read from an external device or use a non-async HTTP library like [requests](https://requests.readthedocs.io/),\nyou should wrap the code in a function and await it with `await rosys.run.io_bound(...)`.\n\nCPU Bound:\nIf you need to do some heavy computation and want to spawn another process,\nyou should wrap the code in a function and await it with `await rosys.run.cpu_bound(...)`.\n\n### Safety\n\nPython is fast enough for most high level logic, but has no realtime guarantees.\nSafety-relevant behavior should therefore be written in [Lizard](https://lizard.dev/) and executed on a suitable microprocessor.\nThe microprocessor governs the hardware of the robot and must be able to perform safety actions like triggering emergency hold etc.\nWe suggest you use an industrial PC with an integrated controller like the [Zauberzeug Robot Brain](https://www.zauberzeug.com/robot-brain.html).\nIt provides a Linux system with AI acceleration to run RoSys, two integrated [ESP32](https://www.espressif.com/en/products/socs/esp32) to run Lizard and six I/O sockets with up to 24 GPIOs for digital I/Os, CAN, RS485, SPI, I2C, ... with a software controllable ENABLE switch.\n\n### User Interface\n\nRoSys plays very well with [NiceGUI](https://nicegui.io/) and provides additional robot-related UI elements.\nNiceGUI is a high-level web UI framework on top of [JustPy](https://justpy.io/).\nThis means you can write all UI code in Python.\nThe state is automatically reflected in the browser through WebSockets.\nRoSys can also be used with other user interfaces or interaction models if required, for example a completely app-based control through Bluetooth Low Energy with Flutter.\n\n### Notifications\n\nModules can notify the user through `rosys.notify(\'message to the user\')`.\nWhen using NiceGUI, the notifications will show as snackbar messages.\nThe history of notifications is stored in the list `rosys.notifications`.\n',
    'author': 'Zauberzeug GmbH',
    'author_email': 'info@zauberzeug.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/zauberzeug/rosys',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<3.12',
}


setup(**setup_kwargs)
