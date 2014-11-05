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

cwindow = ctypes.CDLL(csfml.module_format % 'system')

Bool = ctypes.c_int

Enum = ctypes.c_int

class _InputStream(ctypes.Structure):
    ReadFunc = ctypes.CFUNCTYPE(ctypes.c_int64,
                                ctypes.c_void_p, #data
                                ctypes.c_int64, #size
                                ctypes.c_void_p) #userdata

    SeekFunc = ctypes.CFUNCTYPE(ctypes.c_int64,
                                ctypes.c_int64, #position
                                ctypes.c_void_p) #userdata

    TellFunc = ctypes.CFUNCTYPE(ctypes.c_int64,
                                ctypes.c_void_p) #userdata

    GetSizeFunc = ctypes.CFUNCTYPE(ctypes.c_int64,
                                   ctypes.c_void_p) #userdata

    _fields_ = [('_read', ReadFunc),
                ('_seek', SeekFunc),
                ('_tell', TellFunc),
                ('_get_size', GetSizeFunc),
                ('_userdata', ctypes.c_void_p)]

class Vector2f(ctypes.Structure):
    _fields_ = [('x', ctypes.c_float), ('y', ctypes.c_float)]

    def __init__(self, *args):
        if len(args) == 1:
            return ctypes.Structure.__init__(self, *args[0])
        else:
            return ctypes.Structure.__init__(self, *args)

    def __iter__(self):
        return iter((self.x, self.y))

    def __repr__(self):
        return 'csfml.system.Vector2f(%s, %s)' % (repr(self.x), repr(self.y))

