#!/usr/bin/env python3
#
# by Kevin J. Walchko 26 Aug 2014
#
# PS4 has 6 axes, 16 buttons, 0 hats (not recognized)

try:
    # brew install sdl2
    # pip install PySDL2
    import sdl2
except ImportError:
    print('You must install SLD2 library for this to work')
    print("  macos: brew install sdl2")
    print("  linux: apt install libsdl-dev")
    print("  pip install PySDL2")

    import sys
    sys.exit(1)

from collections import namedtuple

Axis = namedtuple("Axis", "x y")
PS4Buttons = namedtuple("PS4Buttons",
    "x circle square triangle share ps options L3 R3 L1 R1 dp_up dp_down dp_left dp_right pad")
JS = namedtuple("JS", "info leftstick rightstick triggers buttons")
JSInfo = namedtuple("JSInfo", "num_buttons num_axes num_hats")

class Joystick:
    def __init__(self, num):
        # init SDL2 and grab joystick
        sdl2.SDL_Init(sdl2.SDL_INIT_JOYSTICK)
        self.js = sdl2.SDL_JoystickOpen(num)

    def setup(self, btns, axes, hats):
        self.info = JSInfo(btns, axes, hats)

    def dump_buttons(self):
        # debug buttons
        print("Buttons")
        sdl2.SDL_JoystickUpdate()
        for i in range(self.info.num_buttons):
            print(f"  {i}: {sdl2.SDL_JoystickGetButton(self.js, i)}")

    def dump_axes(self):
        # debug axes
        print("Axes")
        sdl2.SDL_JoystickUpdate()
        for i in range(self.info.num_axes):
            print(f"  {i}: {sdl2.SDL_JoystickGetAxis(self.js, i) / 32768}")

class PS4Joystick(Joystick):
    """
    Joystick class setup to handle a Playstation PS4 Controller. If no joystick
    is found, the self.valid is False. If it is not valid, then any returned
    dictionaries will contain all 0 values.
    Buttons     Index number
    --------------------------
        X       = 0
        Circle  = 1
        Square  = 2
        Triangle= 3
        Share   = 4
        PS      = 5
        Options = 6
        L3      = 7
        R3      = 8
        L1      = 9
        R1      = 10
        DPup    = 11
        DPdown  = 12
        DPleft  = 13
        DPright = 14
        PadPress= 15

    Axes
    ---------------------------
        LeftStickX      = X-Axis
        LeftStickY      = Y-Axis (Inverted?)
        RightStickX     = 3rd Axis
        RightStickY     = 4th Axis (Inverted?)
        L2              = 5th Axis (-1.0f to 1.0f range, unpressed is -1.0f, shifted to 0-2)
        R2              = 6th Axis (-1.0f to 1.0f range, unpressed is -1.0f, shifted to 0-2)

    WARNING: doesn't work as a process
    """
    def __init__(self, num=0):

        super().__init__(num)

        # grab info for display
        a = sdl2.SDL_JoystickNumAxes(self.js)
        b = sdl2.SDL_JoystickNumButtons(self.js)
        h = sdl2.SDL_JoystickNumHats(self.js)

        super().setup(b,a,h) # buttons, axes, hats

        if a == -1:
            print('*** No Joystick found ***')
            self.valid = False
        else:
            print('==========================================')
            print(' PS4 Joystick ')
            print('   axes:', a, 'buttons:', b, 'hats:', h)
            print('==========================================')
            self.valid = True

    def __del__(self):
        # clean-up
        if self.valid:
            self.stop()
        print('Bye ...')

    def stop(self):
        sdl2.SDL_JoystickClose(self.js)
        self.valid = False

    def get(self):
        # ps4 = self.ps4
        js = self.js

        sdl2.SDL_JoystickUpdate()

        # these don't work :(
        # accels
        # x = sdl2.SDL_JoystickGetAxis(js, 6) / 32768
        # y = sdl2.SDL_JoystickGetAxis(js, 7) / 32768
        # z = sdl2.SDL_JoystickGetAxis(js, 8) / 32768
        # ps4["axes"] = [x, y, z]
        #
        # # gyros
        # x = sdl2.SDL_JoystickGetAxis(js, 9) / 32768
        # y = sdl2.SDL_JoystickGetAxis(js, 10) / 32768
        # z = sdl2.SDL_JoystickGetAxis(js, 11) / 32768
        # ps4.axes.gyros = [x, y, z]
        #
        # # get hat - doesn't work
        # # [up right down left] = [1 2 4 8]
        # print("hat", sdl2.SDL_JoystickGetHat(js, 0), "\n")
        # print('b 13', sdl2.SDL_JoystickGetButton(js, 13))


        # # debug buttons
        # print("Buttons")
        # for i in range(self.ps4["num_buttons"]):
        #     print(f"  {i}: {sdl2.SDL_JoystickGetButton(js, i)}")

        vals = [True if sdl2.SDL_JoystickGetButton(js, i) else False for i in range(self.info.num_buttons)]
        buttons = PS4Buttons(*vals)

        ps4 = JS(
            self.info, # joystick info
            Axis( # left stick
                sdl2.SDL_JoystickGetAxis(js, 0) / 32768,
                sdl2.SDL_JoystickGetAxis(js, 1) / 32768
            ),
            Axis( # right stick
                sdl2.SDL_JoystickGetAxis(js, 2) / 32768,
                sdl2.SDL_JoystickGetAxis(js, 3) / 32768
            ),
            Axis( # triggers L2 R2
                sdl2.SDL_JoystickGetAxis(js, 4) / 32768 + 1,
                sdl2.SDL_JoystickGetAxis(js, 5) / 32768 + 1
            ),
            buttons
        )

        return ps4


def main():
    import time

    js = PS4Joystick()

    while js.valid:
        try:
            # ps4 = js.get()
            # print(ps4,"\n----------------------\n")
            # time.sleep(0.1)
            # if ps4.buttons.pad is True:
            #     break

            js.dump_buttons()
            js.dump_axes()

        except KeyboardInterrupt:
            print('js exiting ...')
            break


if __name__ == "__main__":
    main()