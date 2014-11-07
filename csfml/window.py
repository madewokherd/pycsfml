# Copyright 2014 Vincent Povirk
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import ctypes

import csfml
import csfml.system

cwindow = ctypes.CDLL(csfml.module_format % 'window')

WindowHandle = csfml.window_handle_type

class ContextSettings(ctypes.Structure):
    _fields_ = [('depth_bits', ctypes.c_uint),
                ('stencil_bits', ctypes.c_uint),
                ('antialiasing_level', ctypes.c_uint),
                ('major_version', ctypes.c_uint),
                ('minor_version', ctypes.c_uint)]

class Event(ctypes.Structure):
    _fields_ = [('event_type', csfml.system.Enum)]

    # FIXME: Add specific event types and conversion to them

class VideoMode(ctypes.Structure):
    _fields_ = [('width', ctypes.c_uint), ('height', ctypes.c_uint), ('bits_per_pixel', ctypes.c_uint)]

    def __init__(self, width=0, height=0, bits_per_pixel=32):
        self.width = width
        self.height = height
        self.bits_per_pixel = bits_per_pixel

    def __iter__(self):
        return iter((self.x, self.y))

    def __repr__(self):
        return 'csfml.window.VideoMode(%s,%s,%s)' % (self.width, self.height, self.bits_per_pixel)

    def is_valid(self):
        return bool(cwindow.sfVideoMode_isValid(self))

    @staticmethod
    def get_desktop_mode():
        return cwindow.sfVideoMode_getDesktopMode()

    @staticmethod
    def get_fullscreen_modes():
        count = ctypes.c_size_t()
        ptr = cwindow.sfVideoMode_getFullscreenModes(ctypes.byref(count))
        return [ptr[i] for i in range(count.value)]

cwindow.sfVideoMode_getDesktopMode.argtypes = []
cwindow.sfVideoMode_getDesktopMode.restype = VideoMode

cwindow.sfVideoMode_getFullscreenModes.argtypes = [ctypes.POINTER(ctypes.c_size_t)]
cwindow.sfVideoMode_getFullscreenModes.restype = ctypes.POINTER(VideoMode)

cwindow.sfVideoMode_isValid.argtypes = [VideoMode]
cwindow.sfVideoMode_isValid.restype = csfml.system.Bool

