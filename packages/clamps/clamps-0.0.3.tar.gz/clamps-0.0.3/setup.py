# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['clamps']

package_data = \
{'': ['*']}

install_requires = \
['PySDL2']

setup_kwargs = {
    'name': 'clamps',
    'version': '0.0.3',
    'description': 'SDL2 joystick driver for python',
    'long_description': '\n![](https://github.com/MomsFriendlyRobotCompany/clamps/blob/master/clamps.png?raw=true)\n\n# clamps\n\n![GitHub](https://img.shields.io/github/license/MomsFriendlyRobotCompany/clamps)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/clamps)\n![PyPI](https://img.shields.io/pypi/v/clamps)\n![PyPI - Downloads](https://img.shields.io/pypi/dm/clamps?color=aqua)\n\n**Note:** I only have playstations, so I don\'t know if this will work with\nother joysticks.\n\nThis is actually something I did long ago, but finally decided to make\nit a module available on PyPi.\n\n## Setup\n\nThis requires `sdl2` inorder to work:\n\n```bash\nbrew install sdl2       # macos\napt install libsdl2-dev # linux\n```\n\nThis package will install the python bindings `PySDL2` from pypi.\n\nTested:\n\n- Works with joystick connected via USB cable\n- Works with joystick connected via bluetooth\n- Works with PS4 controller\n\n## Example\n\n```python\n#!/usr/bin/env python3\nimport time\nfrom clamps import PS4Joystick\n\ndef main():\n    import time\n\n    js = PS4Joystick()\n\n    while js.valid:\n        try:\n            ps4 = js.get()\n            print(ps4,"\\n----------------------\\n")\n            time.sleep(0.1)\n            if ps4.buttons.pad is True:\n                break\n        except KeyboardInterrupt:\n            print(\'js exiting ...\')\n            break\n\n\nif __name__ == "__main__":\n    main()\n```\n\nOutput of `get()` is a `namedtuple` with the following fields:\n\n```python\nJS(info=JSInfo(num_buttons=16, num_axes=6, num_hats=0), leftstick=Axis(x=-0.003936767578125, y=0.011749267578125), rightstick=Axis(x=-0.01177978515625, y=-0.050994873046875), triggers=Axis(x=0.0, y=0.0), buttons=PS4Buttons(x=False, circle=False, square=False, triangle=False, share=False, ps=False, options=False, L3=False, R3=False, L1=False, R1=False, dp_up=False, dp_down=False, dp_left=False, dp_right=False, pad=True))\n```\n\n## [How to pair a DUALSHOCK 4 wireless controller with a supported device][ref]\n\nTo pair your wireless controller with a supported device using Bluetooth for the first time, turn on pairing mode.\n\n1. Make sure the player indicator on the controller is off.\nIf the player indicator is on, press and hold the PS button until it turns off. If a USB is connected to the controller, disconnect it.\n1. While pressing and holding the SHARE button, press and hold the PS Button until the light bar flashes.\n1. Enable Bluetooth on your device, and then select the controller from the list of Bluetooth devices. When pairing is complete, the light bar blinks, and then the player indicator lights up.\n\n\n![](https://github.com/MomsFriendlyRobotCompany/clamps/blob/master/js.webp?raw=true)\n\n[ref]: https://www.playstation.com/en-us/support/hardware/ps4-pair-dualshock-4-wireless-with-pc-or-mac/\n\n\n\n# MIT License\n\n**Copyright (c) 2014 Kevin Walchko**\n\nPermission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:\n\nThe above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.\n\nTHE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.',
    'author': 'walchko',
    'author_email': 'walchko@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://pypi.org/project/clamps/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)
