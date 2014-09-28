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
import csfml.window

cgraphics = ctypes.CDLL(csfml.module_format % 'graphics')

class Color(ctypes.Structure):
    _fields_ = [('r', ctypes.c_uint8), ('g', ctypes.c_uint8), ('b', ctypes.c_uint8), ('a', ctypes.c_uint8)]

    def __init__(self, r, g, b, a=255):
        self.r = r
        self.g = g
        self.b = b
        self.a = a

    def __repr__(self):
        return 'csfml.graphics.Color(%s,%s,%s,%s)' % (self.r, self.g, self.b, self.a)

    def __mul__(self, oth):
        return cgraphics.sfColor_modulate(self, oth)

    def __add__(self, oth):
        return cgraphics.sfColor_add(self, oth)

class Drawable(ctypes.c_void_p):
    def draw(self, render_target, render_states):
        raise NotImplementedError()

class Transform(ctypes.Structure):
    _fields_ = [('matrix', ctypes.c_float * 9)]

    def __repr__(self):
        return 'csfml.graphics.Transform(%s)' % ','.join(repr(x) for x in self.matrix)

class Transformable(ctypes.c_void_p):
    def __new__(self):
        return cgraphics.sfTransformable_create()

    def copy(self):
        return cgraphics.sfTransformable_copy(self)

    def __del__(self):
        cgraphics.sfTransformable_destroy(self)

    def set_position(self, *pos):
        cgraphics.sfTransformable_setPosition(self, csfml.system.Vector2f(*pos))

    def set_rotation(self, angle):
        cgraphics.sfTransformable_setRotation(self, angle)

    def set_scale(self, *scale):
        cgraphics.sfTransformable_setScale(self, csfml.system.Vector2f(*scale))

    def set_origin(self, *origin):
        cgraphics.sfTransformable_setOrigin(self, csfml.system.Vector2f(*origin))

    def get_position(self):
        return cgraphics.sfTransformable_getPosition(self)

    def get_rotation(self):
        return cgraphics.sfTransformable_getRotation(self)

    def get_scale(self):
        return cgraphics.sfTransformable_getScale(self)

    def get_origin(self):
        return cgraphics.sfTransformable_getOrigin(self)

    def move(self, *offset):
        return cgraphics.sfTransformable_move(self, csfml.system.Vector2f(*offset))

    def rotate(self, angle):
        return cgraphics.sfTransformable_rotate(self, angle)

    def scale(self, *factors):
        return cgraphics.sfTransformable_scale(self, csfml.system.Vector2f(*factors))

    def get_transform(self):
        return cgraphics.sfTransformable_getTransform(self)

    def get_inverse_transform(self):
        return cgraphics.sfTransformable_getInverseTransform(self)

    position = property(get_position, set_position)

    rotation = property(get_rotation, set_rotation)

    scale = property(get_scale, set_scale)

    origin = property(get_origin, set_origin)

Color.black = Color.in_dll(cgraphics, 'sfBlack')
Color.white = Color.in_dll(cgraphics, 'sfWhite')
Color.red = Color.in_dll(cgraphics, 'sfRed')
Color.green = Color.in_dll(cgraphics, 'sfGreen')
Color.blue = Color.in_dll(cgraphics, 'sfBlue')
Color.yellow = Color.in_dll(cgraphics, 'sfYellow')
Color.magenta = Color.in_dll(cgraphics, 'sfMagenta')
Color.cyan = Color.in_dll(cgraphics, 'sfCyan')
Color.transparent = Color.in_dll(cgraphics, 'sfTransparent')

Transform.identity = Transform.in_dll(cgraphics, 'sfTransform_Identity')

cgraphics.sfColor_add.argtypes = [Color, Color]
cgraphics.sfColor_add.restype = Color

cgraphics.sfColor_modulate.argtypes = [Color, Color]
cgraphics.sfColor_modulate.restype = Color

cgraphics.sfTransformable_create.argtypes = []
cgraphics.sfTransformable_create.restype = Transformable

cgraphics.sfTransformable_copy.argtypes = [Transformable]
cgraphics.sfTransformable_copy.restype = Transformable

cgraphics.sfTransformable_destroy.argtypes = [Transformable]
cgraphics.sfTransformable_destroy.restype = None

cgraphics.sfTransformable_setPosition.argtypes = [Transformable, csfml.system.Vector2f]
cgraphics.sfTransformable_setPosition.restype = None

cgraphics.sfTransformable_setRotation.argtypes = [Transformable, ctypes.c_float]
cgraphics.sfTransformable_setRotation.restype = None

cgraphics.sfTransformable_setScale.argtypes = [Transformable, csfml.system.Vector2f]
cgraphics.sfTransformable_setScale.restype = None

cgraphics.sfTransformable_setOrigin.argtypes = [Transformable, csfml.system.Vector2f]
cgraphics.sfTransformable_setOrigin.restype = None

cgraphics.sfTransformable_getPosition.argtypes = [Transformable]
cgraphics.sfTransformable_getPosition.restype = csfml.system.Vector2f

cgraphics.sfTransformable_getRotation.argtypes = [Transformable]
cgraphics.sfTransformable_getRotation.restype = ctypes.c_float

cgraphics.sfTransformable_getScale.argtypes = [Transformable]
cgraphics.sfTransformable_getScale.restype = csfml.system.Vector2f

cgraphics.sfTransformable_getOrigin.argtypes = [Transformable]
cgraphics.sfTransformable_getOrigin.restype = csfml.system.Vector2f

cgraphics.sfTransformable_move.argtypes = [Transformable, csfml.system.Vector2f]
cgraphics.sfTransformable_move.restype = None

cgraphics.sfTransformable_rotate.argtypes = [Transformable, ctypes.c_float]
cgraphics.sfTransformable_rotate.restype = None

cgraphics.sfTransformable_scale.argtypes = [Transformable, csfml.system.Vector2f]
cgraphics.sfTransformable_scale.restype = None

cgraphics.sfTransformable_getTransform.argtypes = [Transformable]
cgraphics.sfTransformable_getTransform.restype = Transform

cgraphics.sfTransformable_getInverseTransform.argtypes = [Transformable]
cgraphics.sfTransformable_getInverseTransform.restype = Transform

