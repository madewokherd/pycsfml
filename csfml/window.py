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

def _to_utf32(s):
    return ctypes.c_char_p(s.encode('utf32'))

class ContextSettings(ctypes.Structure):
    _fields_ = [('depth_bits', ctypes.c_uint),
                ('stencil_bits', ctypes.c_uint),
                ('antialiasing_level', ctypes.c_uint),
                ('major_version', ctypes.c_uint),
                ('minor_version', ctypes.c_uint)]

    def __init__(self, depth_bits=0, stencil_bits=0, antialiasing_level=0, major_version=2, minor_version=0):
        ctypes.Structure.__init__(self, depth_bits, stencil_bits, antialiasing_level, major_version, minor_version)

class KeyEvent(ctypes.Structure):
    _fields_ = [('type', csfml.system.Enum),
                ('code', csfml.system.Enum),
                ('alt', csfml.system.Bool),
                ('control', csfml.system.Bool),
                ('shift', csfml.system.Bool),
                ('system', csfml.system.Bool)]

class TextEvent(ctypes.Structure):
    _fields_ = [('type', csfml.system.Enum),
                ('unicode', ctypes.POINTER(ctypes.c_uint32))]

class MouseMoveEvent(ctypes.Structure):
    _fields_ = [('type', csfml.system.Enum),
                ('x', ctypes.c_int),
                ('y', ctypes.c_int)]

class MouseButtonEvent(ctypes.Structure):
    _fields_ = [('type', csfml.system.Enum),
                ('button', csfml.system.Enum),
                ('x', ctypes.c_int),
                ('y', ctypes.c_int)]

class MouseWheelEvent(ctypes.Structure):
    _fields_ = [('type', csfml.system.Enum),
                ('delta', ctypes.c_int),
                ('x', ctypes.c_int),
                ('y', ctypes.c_int)]

class JoystickMoveEvent(ctypes.Structure):
    _fields_ = [('type', csfml.system.Enum),
                ('joystick_id', ctypes.c_uint),
                ('axis', csfml.system.Enum),
                ('position', ctypes.c_float)]

class JoystickButtonEvent(ctypes.Structure):
    _fields_ = [('type', csfml.system.Enum),
                ('joystick_id', ctypes.c_uint),
                ('button', ctypes.c_uint)]

class JoystickConnectEvent(ctypes.Structure):
    _fields_ = [('type', csfml.system.Enum),
                ('joystick_id', ctypes.c_uint)]

class SizeEvent(ctypes.Structure):
    _fields_ = [('type', csfml.system.Enum),
                ('width', ctypes.c_uint),
                ('height', ctypes.c_uint)]

class Event(ctypes.Union):
    _fields_ = [('type', csfml.system.Enum),
                ('size', SizeEvent),
                ('key', KeyEvent),
                ('text', TextEvent),
                ('mouse_move', MouseMoveEvent),
                ('mouse_button', MouseButtonEvent),
                ('mouse_wheel', MouseWheelEvent),
                ('joystick_move', JoystickMoveEvent),
                ('joystick_button', JoystickButtonEvent),
                ('joystick_connect', JoystickConnectEvent)]

    Closed = 0
    Resized = 1
    LostFocus = 2
    GainedFocus = 3
    TextEntered = 4
    KeyPressed = 5
    KeyReleased = 6
    MouseWheelMoved = 7
    MouseButtonPressed = 8
    MouseButtonReleased = 9
    MouseMoved = 10
    MouseEntered = 11
    MouseLeft = 12
    JoystickButtonPressed = 13
    JoystickButtonReleased = 14
    JoystickMoved = 15
    JoystickConnected = 16
    JoystickDisconnected = 17

    _event_type_fields = [None, # Closed
                          'size', # Resized
                          None, # LostFocus
                          None, # GainedFocus
                          'text', # TextEntered
                          'key', # KeyPressed
                          'key', # KeyReleased
                          'mouse_wheel', # MouseWheelMoved
                          'mouse_button', # MouseButtonPressed
                          'mouse_button', # MouseButtonReleased
                          'mouse_move', # MouseMoved
                          None, # MouseEntered
                          None, # MouseLeft
                          'joystick_button', # JoystickButtonPressed
                          'joystick_button', # JoystickButtonReleased
                          'joystick_move', # JoystickMoved
                          'joystick_connect', # JoystickConnected
                          'joystick_connect'] # JoystickDisconnected

    def get_specific_event(self):
        if 0 <= self.type < len(self._event_type_fields):
            field_name = self._event_type_fields[self.type]
            if field_name is not None:
                return getattr(self, field_name)
        return self

class Style(csfml.system.Enum):
    NoStyle = 0
    Titlebar = 1 << 0
    Resize = 1 << 1
    Close = 1 << 2
    Fullscreen = 1 << 3
    Default = Titlebar | Resize | Close

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

class Window(ctypes.c_void_p):
    def __init__(self, mode, title, style=Style.Default, settings=ContextSettings()):
        result = cwindow.sfWindow_createUnicode(mode, _to_utf32(title), style, ctypes.byref(settings))
        self.value = result.value
        result.value = 0

    @staticmethod
    def from_handle(self, handle, settings):
        return cwindow.sfWindow_createFromHandle(handle, ctypes.byref(settings))

    def __del__(self):
        if self.value != 0:
            cwindow.sfWindow_destroy(self)
            self.value = 0

    def close(self):
        cwindow.sfWindow_close(self)

    def is_open(self):
        return bool(cwindow.sfWindow_isOpen(self))

    def get_settings(self):
        return cwindow.sfWindow_getSettings(self)

    settings = property(get_settings)

    def poll_event(self):
        result = Event()
        if cwindow.sfWindow_pollEvent(self, ctypes.byref(result)):
            return result.get_specific_event()

    def wait_event(self):
        result = Event()
        if cwindow.sfWindow_waitEvent(self, ctypes.byref(result)):
            return result.get_specific_event()

    def get_position(self):
        return cwindow.sfWindow_getPosition(self)

    def set_position(self, *position):
        cwindow.sfWindow_setPosition(self, csfml.system.Vector2i(*position))

    position = property(get_position, set_position)

    def get_size(self):
        return cwindow.sfWindow_getSize(self)

    def set_size(self, *size):
        cwindow.sfWindow_setSize(self, csfml.system.Vector2u(*size))

    size = property(get_size, set_size)

    def set_title(self, title):
        cwindow.sfWindow_setUnicodeTitle(self, _to_utf32(title))

    def set_icon(self, width, height, pixels):
        cwindow.sfWindow_setIcon(self, width, height, pixels)

    def set_visible(self, visible):
        cwindow.sfWindow_setVisible(self, visible)

    def set_mouse_cursor_visible(self, visible):
        cwindow.sfWindow_setMouseCursorVisible(self, visible)

    def set_vertical_sync_enabled(self, enabled):
        cwindow.sfWindow_setVerticalSyncEnabled(self, enabled)

    def set_key_repeat_enabled(self, enabled):
        cwindow.sfWindow_setKeyRepeatEnabled(self, enabled)

    def set_active(self, active):
        return bool(cwindow.sfWindow_setActive(self, active))

    def display(self):
        cwindow.sfWindow_display(self)

    def set_framerate_limit(self, limit):
        cwindow.sfWindow_setFramerateLimit(self, limit)

    def set_joystick_threshold(self, threshold):
        cwindow.sfWindow_setJoystickThreshold(self, threshold)

    def get_system_handle(self):
        return cwindow.sfWindow_getSystemHandle(self)

cwindow.sfVideoMode_getDesktopMode.argtypes = []
cwindow.sfVideoMode_getDesktopMode.restype = VideoMode

cwindow.sfVideoMode_getFullscreenModes.argtypes = [ctypes.POINTER(ctypes.c_size_t)]
cwindow.sfVideoMode_getFullscreenModes.restype = ctypes.POINTER(VideoMode)

cwindow.sfVideoMode_isValid.argtypes = [VideoMode]
cwindow.sfVideoMode_isValid.restype = csfml.system.Bool

cwindow.sfWindow_create.argtypes = [VideoMode, ctypes.c_char_p, ctypes.c_uint32, ctypes.POINTER(ContextSettings)]
cwindow.sfWindow_create.restype = Window

cwindow.sfWindow_createUnicode.argtypes = [VideoMode, ctypes.c_char_p, ctypes.c_uint32, ctypes.POINTER(ContextSettings)]
cwindow.sfWindow_createUnicode.restype = Window

cwindow.sfWindow_createFromHandle.argtypes = [WindowHandle, ctypes.POINTER(ContextSettings)]
cwindow.sfWindow_createFromHandle.restype = Window

cwindow.sfWindow_destroy.argtypes = [Window]
cwindow.sfWindow_destroy.restype = None

cwindow.sfWindow_close.argtypes = [Window]
cwindow.sfWindow_close.restype = None

cwindow.sfWindow_isOpen.argtypes = [Window]
cwindow.sfWindow_isOpen.restype = csfml.system.Bool

cwindow.sfWindow_getSettings.argtypes = [Window]
cwindow.sfWindow_getSettings.restype = ContextSettings

cwindow.sfWindow_pollEvent.argtypes = [Window, ctypes.POINTER(Event)]
cwindow.sfWindow_pollEvent.restype = csfml.system.Bool

cwindow.sfWindow_waitEvent.argtypes = [Window, ctypes.POINTER(Event)]
cwindow.sfWindow_waitEvent.restype = csfml.system.Bool

cwindow.sfWindow_getPosition.argtypes = [Window]
cwindow.sfWindow_getPosition.restype = csfml.system.Vector2i

cwindow.sfWindow_setPosition.argtypes = [Window, csfml.system.Vector2i]
cwindow.sfWindow_setPosition.restype = None

cwindow.sfWindow_getSize.argtypes = [Window]
cwindow.sfWindow_getSize.restype = csfml.system.Vector2u

cwindow.sfWindow_setSize.argtypes = [Window, csfml.system.Vector2u]
cwindow.sfWindow_setSize.restype = None

cwindow.sfWindow_setTitle.argtypes = [Window, ctypes.c_char_p]
cwindow.sfWindow_setTitle.restype = None

cwindow.sfWindow_setUnicodeTitle.argtypes = [Window, ctypes.c_char_p]
cwindow.sfWindow_setUnicodeTitle.restype = None

cwindow.sfWindow_setIcon.argtypes = [Window, ctypes.c_uint, ctypes.c_uint, ctypes.POINTER(ctypes.c_uint8)]
cwindow.sfWindow_setIcon.restype = None

cwindow.sfWindow_setVisible.argtypes = [Window, csfml.system.Bool]
cwindow.sfWindow_setVisible.restype = None

cwindow.sfWindow_setMouseCursorVisible.argtypes = [Window, csfml.system.Bool]
cwindow.sfWindow_setMouseCursorVisible.restype = None

cwindow.sfWindow_setVerticalSyncEnabled.argtypes = [Window, csfml.system.Bool]
cwindow.sfWindow_setVerticalSyncEnabled.restype = None

cwindow.sfWindow_setKeyRepeatEnabled.argtypes = [Window, csfml.system.Bool]
cwindow.sfWindow_setKeyRepeatEnabled.restype = None

cwindow.sfWindow_setActive.argtypes = [Window, csfml.system.Bool]
cwindow.sfWindow_setActive.restype = csfml.system.Bool

cwindow.sfWindow_display.argtypes = [Window]
cwindow.sfWindow_display.restype = None

cwindow.sfWindow_setFramerateLimit.argtypes = [Window, ctypes.c_uint]
cwindow.sfWindow_setFramerateLimit.restype = None

cwindow.sfWindow_setJoystickThreshold.argtypes = [Window, ctypes.c_float]
cwindow.sfWindow_setJoystickThreshold.restype = None

cwindow.sfWindow_getSystemHandle.argtypes = [Window]
cwindow.sfWindow_getSystemHandle.restype = WindowHandle

