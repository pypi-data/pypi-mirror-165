#!/usr/bin/env python3

from clamps import Joystick

def main():
    import time

    js = Joystick(0)
    n = 0

    while js.valid:
        try:
            js.dump_axes()
            js.dump_buttons()

            print(f"{n} ----------------------\n")
            time.sleep(0.1)
            # if ps4.buttons.pad is True:
            #     break

            # js.dump_buttons()
            # js.dump_axes()
            n += 1

        except KeyboardInterrupt:
            print('js exiting ...')
            break


if __name__ == "__main__":
    main()