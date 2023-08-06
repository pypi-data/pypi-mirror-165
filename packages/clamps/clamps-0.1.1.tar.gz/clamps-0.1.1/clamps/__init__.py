# -*- coding: utf-8 -*-
##############################################
# The MIT License (MIT)
# Copyright (c) 2014 Kevin Walchko
# see LICENSE for full details
##############################################
from .js import PS4Joystick
from .js import PS5Joystick
from .js import Joystick
from .js import Axis, PSButtons, JS, JSInfo

from importlib.metadata import version # type: ignore

__author__ = "Kevin Walchko"
__license__ = "MIT"
__version__ = version("clamps")