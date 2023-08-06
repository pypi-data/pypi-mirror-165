
![](https://github.com/MomsFriendlyRobotCompany/clamps/blob/main/clamps.png?raw=true)

# clamps

![GitHub](https://img.shields.io/github/license/MomsFriendlyRobotCompany/clamps)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/clamps)
![PyPI](https://img.shields.io/pypi/v/clamps)
![PyPI - Downloads](https://img.shields.io/pypi/dm/clamps?color=aqua)

**Note:** I only have playstations, so I don't know if this will work with
other joysticks.

This is actually something I did long ago, but finally decided to make
it a module available on PyPi.

## Setup

This requires `sdl2` inorder to work:

```bash
brew install sdl2       # macos
apt install libsdl2-dev # linux
```

This package will install the python bindings `PySDL2` from pypi.

Tested:

- Works with joystick connected via USB cable
- Works with joystick connected via bluetooth
- Works with PS4 controller
- Works with PS5 controller

## Example

So really, there is no difference between `PS4Joystick` amd `PS5Joystick`,
but both classes exist. Originally I hoped there would be a difference,
like access to the gyros and accelerometers, but there isn't.

```python
#!/usr/bin/env python3
import time
from clamps import PS4Joystick

def main():
    import time

    js = PS4Joystick() # or PS5Joystick()

    while js.valid:
        try:
            ps4 = js.get()
            print(ps4,"\n----------------------\n")
            time.sleep(0.1)
            if ps4.buttons.pad is True:
                break
        except KeyboardInterrupt:
            print('js exiting ...')
            break


if __name__ == "__main__":
    main()
```

Output of `get()` is a `namedtuple` with the following fields:

```python
JS(info=JSInfo(num_buttons=16, num_axes=6, num_hats=0), leftstick=Axis(x=-0.003936767578125, y=0.011749267578125), rightstick=Axis(x=-0.01177978515625, y=-0.050994873046875), triggers=Axis(x=0.0, y=0.0), buttons=PS4Buttons(x=False, circle=False, square=False, triangle=False, share=False, ps=False, options=False, L3=False, R3=False, L1=False, R1=False, dp_up=False, dp_down=False, dp_left=False, dp_right=False, pad=True))
```

## [How to pair a DUALSHOCK 4 wireless controller with a supported device][ref]

To pair your wireless controller with a supported device using Bluetooth for the first time, turn on pairing mode.

1. Make sure the player indicator on the controller is off.
If the player indicator is on, press and hold the PS button until it turns off. If a USB is connected to the controller, disconnect it.
1. While pressing and holding the SHARE button, press and hold the PS Button until the light bar flashes.
1. Enable Bluetooth on your device, and then select the controller from the list of Bluetooth devices. When pairing is complete, the light bar blinks, and then the player indicator lights up.


![](https://github.com/MomsFriendlyRobotCompany/clamps/blob/main/js.webp?raw=true)

[ref]: https://www.playstation.com/en-us/support/hardware/ps4-pair-dualshock-4-wireless-with-pc-or-mac/



# MIT License

**Copyright (c) 2014 Kevin Walchko**

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
