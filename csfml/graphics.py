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

class BlendMode(csfml.system.Enum):
    BlendAlpha = 0
    BlendAdd = 1
    BlendMultiply = 2
    BlendNone = 3

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

class FloatRect(ctypes.Structure):
    _fields_ = [('left', ctypes.c_float), ('top', ctypes.c_float), ('width', ctypes.c_float), ('height', ctypes.c_float)]

    @staticmethod
    def from_vectors(position, size):
       return FloatRect(position.x, position.y, size.x, size.y)

    def __repr__(self):
        return 'csfml.graphics.FloatRect(%s,%s,%s,%s)' % (self.left, self.top, self.width, self.height)

    def __contains__(self, vector):
        return bool(cgraphics.sfFloatRect_contains(ctypes.byref(self), *vector))

    contains = __contains__

    def intersects(self, other):
        intersection = FloatRect()
        if cgraphics.sfFloatRect_intersects(ctypes.byref(self), ctypes.byref(other), ctypes.byref(intersection)):
            return intersection

class Font(ctypes.c_void_p):
    def __init__(self, filename):
        result = cgraphics.sfFont_createFromFile(filename)
        self.value = result.value
        result.value = 0

    @staticmethod
    def from_file(filename):
        return cgraphics.sfFont_createFromFile(filename)

    @staticmethod
    def from_memory(data, size):
        return cgraphics.sfFont_createFromMemory(data, size)

    @staticmethod
    def from_stream(stream):
        return cgraphics.sfFont_createFromStream(stream)

    def copy(self):
        return cgraphics.sfFont_copy(self)

    def __del__(self):
        if self.value != 0:
            cgraphics.sfFont_destroy(self)
            self.value = 0

    def get_glyph(self, code_point, character_size, bold):
        return cgraphics.sfFont_getGlyph(self, code_point, character_size, bold)

    def get_kerning(self, first, second, character_size):
        return cgraphics.sfFont_getKerning(self, first, second, character_size)

    def get_line_spacing(self, character_size):
        return cgraphics.sfFont_getLineSpacing(self, character_size)

    def get_texture(self, character_size):
        result = cgraphics.sfFont_getTexture(self, character_size)
        result._const = True
        return result

class Image(ctypes.c_void_p):
    def __init__(self, width, height):
        res = cgraphics.sfImage_create(width, height)
        self.value = res.value
        res.value = 0

    @staticmethod
    def from_color(width, height, color):
        return cgraphics.sfImage_createFromColor(width, height, color)

    @staticmethod
    def from_pixels(width, height, pixels):
        return cgraphics.sfImage_createFromPixels(width, height, pixels)

    @staticmethod
    def from_file(filename):
        return cgraphics.sfImage_createFromFile(filename)

    @staticmethod
    def from_memory(data, size):
        return cgraphics.sfImage_createFromMemory(data, size)

    @staticmethod
    def from_stream(stream):
        return cgraphics.sfImage_createFromStream(stream)

    def copy(self):
        return cgraphics.sfImage_copy(self)

    def __del__(self):
        if self.value != 0:
            cgraphics.sfImage_destroy(self)
            self.value = 0

    def save_to_file(self, filename):
        if not cgraphics.sfImage_saveToFile(self, filename):
            raise Exception("save failed")

    def get_size(self):
        return cgraphics.sfImage_getSize(self)

    def get_width(self):
        return cgraphics.sfImage_getSize(self).x

    def get_height(self):
        return cgraphics.sfImage_getSize(self).y

    size = property(get_size)

    width = property(get_width)

    height = property(get_height)

    def create_mask_from_color(self, color, alpha):
        cgraphics.sfImage_createMaskFromColor(self, color, alpha)

    def copy_image(self, source, dest_x, dest_y, source_rect, apply_alpha):
        cgraphics.sfImage_copyImage(self, source, dest_x, dest_y, source_rect, apply_alpha)

    def set_pixel(self, x, y, color):
        cgraphics.sfImage_setPixel(self, x, y, color)

    def get_pixel(self, x, y):
        return cgraphics.sfImage_getPixel(self, x, y)

    def get_pixels_ptr(self):
        return cgraphics.sfImage_getPixelsPtr(self)

    def flip_horizontally(self):
        cgraphics.sfImage_flipHorizontally(self)

    def flip_vertically(self):
        cgraphics.sfImage_flipVertically(self)

class IntRect(ctypes.Structure):
    _fields_ = [('left', ctypes.c_int), ('top', ctypes.c_int), ('width', ctypes.c_int), ('height', ctypes.c_int)]

    @staticmethod
    def from_vectors(position, size):
       return IntRect(position.x, position.y, size.x, size.y)

    def __repr__(self):
        return 'csfml.graphics.IntRect(%s,%s,%s,%s)' % (self.left, self.top, self.width, self.height)

    def __contains__(self, vector):
        return bool(cgraphics.sfIntRect_contains(ctypes.byref(self), *vector))

    contains = __contains__

    def intersects(self, other):
        intersection = IntRect()
        if cgraphics.sfIntRect_intersects(ctypes.byref(self), ctypes.byref(other), ctypes.byref(intersection)):
            return intersection

class Glyph(ctypes.Structure):
    _fields_ = [('advance', ctypes.c_int),
                ('bounds', IntRect),
                ('texture_rect', IntRect)]

RenderWindow = ctypes.c_void_p # FIXME

class Shader(ctypes.c_void_p):
    def __init__(self):
        raise TypeError("use Shader.from_file, Shader.from_memory, or Shader.from_stream")

    @staticmethod
    def from_file(vertex_shader_filename, fragment_shader_filename):
        return cgraphics.sfShader_createFromFile(vertex_shader_filename, fragment_shader_filename)

    @staticmethod
    def from_memory(vertex_shader, fragment_shader):
        return cgraphics.sfShader_createFromMemory(vertex_shader, fragment_shader)

    @staticmethod
    def from_stream(vertex_shader_stream, fragment_shader_stream):
        return cgraphics.sfShader_createFromStream(vertex_shader_stream, fragment_shader_stream)

    def __del__(self):
        if self.value != 0:
            cgraphics.sfShader_destroy(self)
            self.value = 0

    # FIXME: Make a "params" object so we can do e.g. 'shader.params.name = 2.0'?

    def set_float_parameter(self, name, x):
        cgraphics.sfShader_setFloatParameter(self, name, x)

    def set_float2_parameter(self, name, x, y):
        cgraphics.sfShader_setFloat2Parameter(self, name, x, y)

    def set_float3_parameter(self, name, x, y, z):
        cgraphics.sfShader_setFloat3Parameter(self, name, x, y, z)

    def set_float4_parameter(self, name, x, y, z, w):
        cgraphics.sfShader_setFloat4Parameter(self, name, x, y, z, w)

    def set_vector2_parameter(self, name, vector):
        cgraphics.sfShader_setVector2Parameter(self, name, vector)

    def set_vector3_parameter(self, name, vector):
        cgraphics.sfShader_setVector3Parameter(self, name, vector)

    def set_color_parameter(self, name, color):
        cgraphics.sfShader_setColorParameter(self, name, color)

    def set_transform_parameter(self, name, transform):
        cgraphics.sfShader_setTransformParameter(self, name, transform)

    def set_texture_parameter(self, name, texture):
        cgraphics.sfShader_setTextureParameter(self, name, texture)

    def set_current_texture_parameter(self, name):
        cgraphics.sfShader_setCurrentTextureParameter(self, name)

    def bind(self):
        cgraphics.sfShader_bind(self)

    @staticmethod
    def is_available():
        return bool(cgraphics.sfShader_isAvailable())

class Sprite(ctypes.c_void_p):
    _owned = True

    def __init__(self):
        result = cgraphics.sfSprite_create()
        self.value = result.value
        result.value = 0

    def copy(self):
        return cgraphics.sfSprite_copy(self)

    def __del__(self):
        if self.value != 0 and self._owned:
            cgraphics.sfSprite_destroy(self)
            self.value = 0

    def set_position(self, *position):
        cgraphics.sfSprite_setPosition(self, csfml.system.Vector2f(*position))

    def set_rotation(self, angle):
        cgraphics.sfSprite_setRotation(self, angle)

    def set_scale(self, *scale):
        cgraphics.sfSprite_setScale(self, csfml.system.Vector2f(*scale))

    def set_origin(self, *origin):
        cgraphics.sfSprite_setOrigin(self, csfml.system.Vector2f(*origin))

    def get_position(self):
        return cgraphics.sfSprite_getPosition(self)

    position = property(get_position, set_position)

    def get_rotation(self):
        return cgraphics.sfSprite_getRotation(self)

    rotation = property(get_rotation, set_rotation)

    def get_scale(self):
        return cgraphics.sfSprite_getScale(self)

    scale = property(get_scale, set_scale)

    def get_origin(self):
        return cgraphics.sfSprite_getOrigin(self)

    origin = property(get_origin, set_origin)

    def move(self, *offset):
        cgraphics.sfSprite_move(self, csfml.system.Vector2f(*offset))

    def rotate(self, angle):
        cgraphics.sfSprite_rotate(self, angle)

    def scale(self, *factors):
        cgraphics.sfSprite_scale(self, csfml.system.Vector2f(*factors))

    def get_transform(self):
        return cgraphics.sfSprite_getTransform(self)

    def get_inverse_transform(self):
        return cgraphics.sfSprite_getInverseTransform(self)

    _texture = None

    def set_texture(self, texture, reset_rect=False):
        cgraphics.sfSprite_setTexture(self, texture, reset_rect)
        self._texture = texture # sfSprite_setTexture doesn't copy the texture, so make sure we keep it around

    def set_texture_rect(self, rectangle):
        cgraphics.sfSprite_setTextureRect(self, rectangle)

    def set_color(self, color):
        cgraphics.sfSprite_setColor(self, color)

    def get_texture(self):
        result = cgraphics.sfSprite_getTexture(self)
        result._const = True
        if self._texture is not None and self._texture.value == result.value:
            return self._texture
        return result

    texture = property(get_texture, set_texture)

    def get_texture_rect(self):
        return cgraphics.sfSprite_getTextureRect(self)

    texture_rect = property(get_texture_rect, set_texture_rect)

    def get_color(self):
        return cgraphics.sfSprite_getColor(self)

    color = property(get_color, set_color)

    def get_local_bounds(self):
        return cgraphics.sfSprite_getLocalBounds(self)

    def get_global_bounds(self):
        return cgraphics.sfSprite_getGlobalBounds(self)

class Texture(ctypes.c_void_p):
    def __init__(self, width, height):
        result = cgraphics.sfTexture_create(width, height)
        self.value = result.value
        result.value = 0

    @staticmethod
    def from_file(filename, area=None):
        if area is None:
            area = POINTER(IntRect)()
        else:
            area = ctypes.byref(area)
        return cgraphics.sfTexture_createFromFile(filename, area)

    @staticmethod
    def from_memory(data, size, area=None):
        if area is None:
            area = POINTER(IntRect)()
        else:
            area = ctypes.byref(area)
        return cgraphics.sfTexture_createFromMemory(data, size, area)

    @staticmethod
    def from_stream(stream, area=None):
        if area is None:
            area = POINTER(IntRect)()
        else:
            area = ctypes.byref(area)
        return cgraphics.sfTexture_createFromStream(stream, area)

    @staticmethod
    def from_image(image, area=None):
        if area is None:
            area = POINTER(IntRect)()
        else:
            area = ctypes.byref(area)
        return cgraphics.sfTexture_createFromImage(image, area)

    def copy(self):
        return cgraphics.sfTexture_copy(self)

    _const = False

    def __del__(self):
        if self.value != 0 and not self._const:
            cgraphics.sfTexture_destroy(self)
            self.value = 0

    def get_size(self):
        return cgraphics.sfTexture_getSize(self)

    def get_width(self):
        return cgraphics.sfTexture_getSize(self).x

    def get_height(self):
        return cgraphics.sfTexture_getSize(self).y

    size = property(get_size)

    width = property(get_width)

    height = property(get_height)

    def copy_to_image(self):
        return cgraphics.sfTexture_copyToImage(self)

    def update_from_pixels(self, pixels, width, height, x, y):
        if self._const:
            raise TypeError("this texture is const")
        cgraphics.sfTexture_updateFromPixels(self, pixels, width, height, x, y)

    def update_from_image(self, image, x, y):
        if self._const:
            raise TypeError("this texture is const")
        cgraphics.sfTexture_updateFromImage(self, image, x, y)

    def update_from_window(self, window, x, y):
        if self._const:
            raise TypeError("this texture is const")
        cgraphics.sfTexture_updateFromWindow(self, window, x, y)

    def update_from_render_window(self, render_window, x, y):
        if self._const:
            raise TypeError("this texture is const")
        cgraphics.sfTexture_updateFromRenderWindow(self, render_window, x, y)

    def set_smooth(self, smooth):
        if self._const:
            raise TypeError("this texture is const")
        cgraphics.sfTexture_setSmooth(self, smooth)

    def is_smooth(self):
        return bool(cgraphics.sfTexture_isSmooth)

    smooth = property(is_smooth, set_smooth)

    def set_repeated(self, repeated):
        if self._const:
            raise TypeError("this texture is const")
        cgraphics.sfTexture_setRepeated(self, repeated)

    def is_repeated(self):
        return bool(cgraphics.sfTexture_isRepeated(self))

    repeated = property(is_repeated, set_repeated)

    def bind(self):
        cgraphics.sfTexture_bind(self)

    @staticmethod
    def get_maximum_size():
        return cgraphics.sfTexture_getMaximumSize()

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

class View(ctypes.c_void_p):
    def __new__(self, *args):
        return cgraphics.sfView_create()

    def __init__(self, rectangle=None):
        if rectangle is not None:
            self.reset(rectangle)

    def copy(self):
        return cgraphics.sfView_copy(self)

    def __del__(self):
        if self.value != 0:
            cgraphics.sfView_destroy(self)
            self.value = 0

    def set_center(self, *center):
        cgraphics.sfView_setCenter(self, csfml.system.Vector2f(*center))

    def set_size(self, *size):
        cgraphics.sfView_setSize(self, csfml.system.Vector2f(*size))

    def set_rotation(self, angle):
        cgraphics.sfView_setRotation(self, angle)

    def set_viewport(self, viewport):
        cgraphics.sfView_setViewport(self, viewport)

    def reset(self, rectangle):
        cgraphics.sfView_reset(self, rectangle)

    def get_center(self):
        return cgraphics.sfView_getCenter(self)

    def get_size(self):
        return cgraphics.sfView_getSize(self)

    def get_rotation(self):
        return cgraphics.sfView_getRotation(self)

    def get_viewport(self):
        return cgraphics.sfView_getViewport(self)

    def move(self, *offset):
        cgraphics.sfView_move(self, csfml.system.Vector2f(*offset))

    def rotate(self, angle):
        cgraphics.sfView_rotate(self, angle)

    def zoom(self, factor):
        cgraphics.sfView_zoom(self, factor)

    center = property(get_center, set_center)
    size = property(get_size, set_size)
    rotation = property(get_rotation, set_rotation)
    viewport = property(get_viewport, set_viewport)

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

class RenderStates(ctypes.Structure):
    _fields_ = [('blend_mode', BlendMode),
                ('transform', Transform),
                ('texture', Texture),
                ('shader', Shader)]

    def __init__(self, blend_mode=BlendMode.BlendAlpha, transform=Transform.identity, texture=None, shader=None):
        ctypes.Structure.__init__(self, blend_mode, transform, texture, shader)

cgraphics.sfColor_add.argtypes = [Color, Color]
cgraphics.sfColor_add.restype = Color

cgraphics.sfColor_modulate.argtypes = [Color, Color]
cgraphics.sfColor_modulate.restype = Color

cgraphics.sfFloatRect_contains.argtypes = [ctypes.POINTER(FloatRect), ctypes.c_float, ctypes.c_float]
cgraphics.sfFloatRect_contains.restype = csfml.system.Bool

cgraphics.sfFloatRect_intersects.argtypes = [ctypes.POINTER(FloatRect), ctypes.POINTER(FloatRect), ctypes.POINTER(FloatRect)]
cgraphics.sfFloatRect_intersects.restype = csfml.system.Bool

cgraphics.sfFont_createFromFile.argtypes = [ctypes.c_char_p]
cgraphics.sfFont_createFromFile.restype = Font

cgraphics.sfFont_createFromMemory.argtypes = [ctypes.c_void_p, ctypes.c_size_t]
cgraphics.sfFont_createFromMemory.restype = Font

cgraphics.sfFont_createFromStream.argtypes = [csfml.system._InputStream]
cgraphics.sfFont_createFromStream.restype = Font

cgraphics.sfFont_copy.argtypes = [Font]
cgraphics.sfFont_copy.restype = Font

cgraphics.sfFont_destroy.argtypes = [Font]
cgraphics.sfFont_destroy.restype = None

cgraphics.sfFont_getGlyph.argtypes = [Font, ctypes.c_uint32, ctypes.c_uint, csfml.system.Bool]
cgraphics.sfFont_getGlyph.restype = Glyph

cgraphics.sfFont_getKerning.argtypes = [Font, ctypes.c_uint32, ctypes.c_uint32, ctypes.c_uint]
cgraphics.sfFont_getKerning.restype = ctypes.c_int

cgraphics.sfFont_getLineSpacing.argtypes = [Font, ctypes.c_uint]
cgraphics.sfFont_getLineSpacing.restype = ctypes.c_int

cgraphics.sfFont_getTexture.argtypes = [Font, ctypes.c_uint]
cgraphics.sfFont_getTexture.restype = Texture

cgraphics.sfImage_create.argtypes = [ctypes.c_uint, ctypes.c_uint]
cgraphics.sfImage_create.restype = Image

cgraphics.sfImage_createFromColor.argtypes = [ctypes.c_uint, ctypes.c_uint, Color]
cgraphics.sfImage_createFromColor.restype = Image

cgraphics.sfImage_createFromPixels.argtypes = [ctypes.c_uint, ctypes.c_uint, ctypes.c_void_p]
cgraphics.sfImage_createFromPixels.restype = Image

cgraphics.sfImage_createFromFile.argtypes = [ctypes.c_char_p]
cgraphics.sfImage_createFromFile.restype = Image

cgraphics.sfImage_createFromMemory.argtypes = [ctypes.c_void_p, ctypes.c_size_t]
cgraphics.sfImage_createFromMemory.restype = Image

cgraphics.sfImage_createFromStream.argtypes = [csfml.system._InputStream]
cgraphics.sfImage_createFromStream.restype = Image

cgraphics.sfImage_copy.argtypes = [Image]
cgraphics.sfImage_copy.restype = Image

cgraphics.sfImage_destroy.argtypes = [Image]
cgraphics.sfImage_destroy.restype = None

cgraphics.sfImage_saveToFile.argtypes = [Image, ctypes.c_char_p]
cgraphics.sfImage_saveToFile.restype = csfml.system.Bool

cgraphics.sfImage_getSize.argtypes = [Image]
cgraphics.sfImage_getSize.restype = csfml.system.Vector2u

cgraphics.sfImage_createMaskFromColor.argtypes = [Image, Color, ctypes.c_uint8]
cgraphics.sfImage_createMaskFromColor.restype = None

cgraphics.sfImage_copyImage.argtypes = [Image, Image, ctypes.c_uint, ctypes.c_uint, IntRect, csfml.system.Bool]
cgraphics.sfImage_copyImage.restype = None

cgraphics.sfImage_setPixel.argtypes = [Image, ctypes.c_uint, ctypes.c_uint, Color]
cgraphics.sfImage_setPixel.restype = None

cgraphics.sfImage_getPixel.argtypes = [Image, ctypes.c_uint, ctypes.c_uint]
cgraphics.sfImage_getPixel.restype = Color

cgraphics.sfImage_getPixelsPtr.argtypes = [Image]
cgraphics.sfImage_getPixelsPtr.restype = ctypes.c_void_p

cgraphics.sfImage_flipHorizontally.argtypes = [Image]
cgraphics.sfImage_flipHorizontally.restype = None

cgraphics.sfImage_flipVertically.argtypes = [Image]
cgraphics.sfImage_flipVertically.restype = None

cgraphics.sfIntRect_contains.argtypes = [ctypes.POINTER(IntRect), ctypes.c_int, ctypes.c_int]
cgraphics.sfIntRect_contains.restype = csfml.system.Bool

cgraphics.sfIntRect_intersects.argtypes = [ctypes.POINTER(IntRect), ctypes.POINTER(IntRect), ctypes.POINTER(IntRect)]
cgraphics.sfIntRect_intersects.restype = csfml.system.Bool

cgraphics.sfShader_createFromFile.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
cgraphics.sfShader_createFromFile.restype = Shader

cgraphics.sfShader_createFromMemory.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
cgraphics.sfShader_createFromMemory.restype = Shader

cgraphics.sfShader_createFromStream.argtypes = [csfml.system._InputStream, csfml.system._InputStream]
cgraphics.sfShader_createFromStream.restype = Shader

cgraphics.sfShader_destroy.argtypes = [Shader]
cgraphics.sfShader_destroy.restype = None

cgraphics.sfShader_setFloatParameter.argtypes = [Shader, ctypes.c_char_p, ctypes.c_float]
cgraphics.sfShader_setFloatParameter.restype = None

cgraphics.sfShader_setFloat2Parameter.argtypes = [Shader, ctypes.c_char_p, ctypes.c_float, ctypes.c_float]
cgraphics.sfShader_setFloat2Parameter.restype = None

cgraphics.sfShader_setFloat3Parameter.argtypes = [Shader, ctypes.c_char_p, ctypes.c_float, ctypes.c_float, ctypes.c_float]
cgraphics.sfShader_setFloat3Parameter.restype = None

cgraphics.sfShader_setFloat4Parameter.argtypes = [Shader, ctypes.c_char_p, ctypes.c_float, ctypes.c_float, ctypes.c_float, ctypes.c_float]
cgraphics.sfShader_setFloat4Parameter.restype = None

cgraphics.sfShader_setVector2Parameter.argtypes = [Shader, ctypes.c_char_p, csfml.system.Vector2f]
cgraphics.sfShader_setVector2Parameter.restype = None

cgraphics.sfShader_setVector3Parameter.argtypes = [Shader, ctypes.c_char_p, csfml.system.Vector3f]
cgraphics.sfShader_setVector3Parameter.restype = None

cgraphics.sfShader_setColorParameter.argtypes = [Shader, ctypes.c_char_p, Color]
cgraphics.sfShader_setColorParameter.restype = None

cgraphics.sfShader_setTransformParameter.argtypes = [Shader, ctypes.c_char_p, Transform]
cgraphics.sfShader_setTransformParameter.restype = None

cgraphics.sfShader_setTextureParameter.argtypes = [Shader, ctypes.c_char_p, Texture]
cgraphics.sfShader_setTextureParameter.restype = None

cgraphics.sfShader_setCurrentTextureParameter.argtypes = [Shader, ctypes.c_char_p]
cgraphics.sfShader_setCurrentTextureParameter.restype = None

cgraphics.sfShader_bind.argtypes = [Shader]
cgraphics.sfShader_bind.restype = None

cgraphics.sfShader_isAvailable.argtypes = []
cgraphics.sfShader_isAvailable.restype = csfml.system.Bool

cgraphics.sfSprite_create.argtypes = []
cgraphics.sfSprite_create.restype = Sprite

cgraphics.sfSprite_copy.argtypes = [Sprite]
cgraphics.sfSprite_copy.restype = Sprite

cgraphics.sfSprite_destroy.argtypes = [Sprite]
cgraphics.sfSprite_destroy.restype = None

cgraphics.sfSprite_setPosition.argtypes = [Sprite, csfml.system.Vector2f]
cgraphics.sfSprite_setPosition.restype = None

cgraphics.sfSprite_setRotation.argtypes = [Sprite, ctypes.c_float]
cgraphics.sfSprite_setRotation.restype = None

cgraphics.sfSprite_setScale.argtypes = [Sprite, csfml.system.Vector2f]
cgraphics.sfSprite_setScale.restype = None

cgraphics.sfSprite_setOrigin.argtypes = [Sprite, csfml.system.Vector2f]
cgraphics.sfSprite_setOrigin.restype = None

cgraphics.sfSprite_getPosition.argtypes = [Sprite]
cgraphics.sfSprite_getPosition.restype = csfml.system.Vector2f

cgraphics.sfSprite_getRotation.argtypes = [Sprite]
cgraphics.sfSprite_getRotation.restype = ctypes.c_float

cgraphics.sfSprite_getScale.argtypes = [Sprite]
cgraphics.sfSprite_getScale.restype = csfml.system.Vector2f

cgraphics.sfSprite_getOrigin.argtypes = [Sprite]
cgraphics.sfSprite_getOrigin.restype = csfml.system.Vector2f

cgraphics.sfSprite_move.argtypes = [Sprite, csfml.system.Vector2f]
cgraphics.sfSprite_move.restype = None

cgraphics.sfSprite_rotate.argtypes = [Sprite, ctypes.c_float]
cgraphics.sfSprite_rotate.restype = None

cgraphics.sfSprite_scale.argtypes = [Sprite, csfml.system.Vector2f]
cgraphics.sfSprite_scale.restype = None

cgraphics.sfSprite_getTransform.argtypes = [Sprite]
cgraphics.sfSprite_getTransform.restype = Transform

cgraphics.sfSprite_getInverseTransform.argtypes = [Sprite]
cgraphics.sfSprite_getInverseTransform.restype = Transform

cgraphics.sfSprite_setTexture.argtypes = [Sprite, Texture, csfml.system.Bool]
cgraphics.sfSprite_setTexture.restype = None

cgraphics.sfSprite_setTextureRect.argtypes = [Sprite, IntRect]
cgraphics.sfSprite_setTextureRect.restype = None

cgraphics.sfSprite_setColor.argtypes = [Sprite, Color]
cgraphics.sfSprite_setColor.restype = None

cgraphics.sfSprite_getTexture.argtypes = [Sprite]
cgraphics.sfSprite_getTexture.restype = Texture

cgraphics.sfSprite_getTextureRect.argtypes = [Sprite]
cgraphics.sfSprite_getTextureRect.restype = IntRect

cgraphics.sfSprite_getColor.argtypes = [Sprite]
cgraphics.sfSprite_getColor.restype = Color

cgraphics.sfSprite_getLocalBounds.argtype = [Sprite]
cgraphics.sfSprite_getLocalBounds.restype = FloatRect

cgraphics.sfSprite_getGlobalBounds.argtype = [Sprite]
cgraphics.sfSprite_getGlobalBounds.restype = FloatRect

cgraphics.sfTexture_create.argtypes = [ctypes.c_uint, ctypes.c_uint]
cgraphics.sfTexture_create.restype = Texture

cgraphics.sfTexture_createFromFile.argtypes = [ctypes.c_char_p, ctypes.POINTER(IntRect)]
cgraphics.sfTexture_createFromFile.restype = Texture

cgraphics.sfTexture_createFromMemory.argtypes = [ctypes.c_void_p, ctypes.c_size_t, ctypes.POINTER(IntRect)]
cgraphics.sfTexture_createFromMemory.restype = Texture

cgraphics.sfTexture_createFromStream.argtypes = [csfml.system._InputStream, ctypes.POINTER(IntRect)]
cgraphics.sfTexture_createFromStream.restype = Texture

cgraphics.sfTexture_createFromImage.argtypes = [Image, ctypes.POINTER(IntRect)]
cgraphics.sfTexture_createFromImage.restype = Texture

cgraphics.sfTexture_copy.argtypes = [Texture]
cgraphics.sfTexture_copy.restype = Texture

cgraphics.sfTexture_destroy.argtypes = [Texture]
cgraphics.sfTexture_destroy.restype = None

cgraphics.sfTexture_getSize.argtypes = [Texture]
cgraphics.sfTexture_getSize.restype = csfml.system.Vector2u

cgraphics.sfTexture_copyToImage.argtypes = [Texture]
cgraphics.sfTexture_copyToImage.restype = Image

cgraphics.sfTexture_updateFromPixels.argtypes = [Texture, ctypes.POINTER(ctypes.c_uint8), ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint]
cgraphics.sfTexture_updateFromPixels.restype = None

cgraphics.sfTexture_updateFromImage.argtypes = [Texture, Image, ctypes.c_uint, ctypes.c_uint]
cgraphics.sfTexture_updateFromImage.restype = None

cgraphics.sfTexture_updateFromWindow.argtypes = [Texture, csfml.window.Window, ctypes.c_uint, ctypes.c_uint]
cgraphics.sfTexture_updateFromWindow.restype = None

cgraphics.sfTexture_updateFromRenderWindow.argtypes = [Texture, RenderWindow, ctypes.c_uint, ctypes.c_uint]
cgraphics.sfTexture_updateFromRenderWindow.restype = None

cgraphics.sfTexture_setSmooth.argtypes = [Texture, csfml.system.Bool]
cgraphics.sfTexture_setSmooth.restype = None

cgraphics.sfTexture_isSmooth.argtypes = [Texture]
cgraphics.sfTexture_isSmooth.restype = csfml.system.Bool

cgraphics.sfTexture_setRepeated.argtypes = [Texture, csfml.system.Bool]
cgraphics.sfTexture_setRepeated.restype = None

cgraphics.sfTexture_isRepeated.argtypes = [Texture]
cgraphics.sfTexture_isRepeated.restype = csfml.system.Bool

cgraphics.sfTexture_bind.argtypes = [Texture]
cgraphics.sfTexture_bind.restype = None

cgraphics.sfTexture_getMaximumSize.argtypes = []
cgraphics.sfTexture_getMaximumSize.restype = ctypes.c_uint

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

cgraphics.sfView_create.argtypes = []
cgraphics.sfView_create.restype = View

cgraphics.sfView_createFromRect.argtypes = [FloatRect]
cgraphics.sfView_createFromRect.restype = View

cgraphics.sfView_copy.argtypes = [View]
cgraphics.sfView_copy.restype = View

cgraphics.sfView_destroy.argtypes = [View]
cgraphics.sfView_destroy.restype = None

cgraphics.sfView_setCenter.argtypes = [View, csfml.system.Vector2f]
cgraphics.sfView_setCenter.restype = None

cgraphics.sfView_setSize.argtypes = [View, csfml.system.Vector2f]
cgraphics.sfView_setSize.restype = None

cgraphics.sfView_setRotation.argtypes = [View, ctypes.c_float]
cgraphics.sfView_setRotation.restype = None

cgraphics.sfView_setViewport.argtypes = [View, FloatRect]
cgraphics.sfView_setViewport.restype = None

cgraphics.sfView_reset.argtypes = [View, FloatRect]
cgraphics.sfView_reset.restype = None

cgraphics.sfView_getCenter.argtypes = [View]
cgraphics.sfView_getCenter.restype = csfml.system.Vector2f

cgraphics.sfView_getSize.argtypes = [View]
cgraphics.sfView_getSize.restype = csfml.system.Vector2f

cgraphics.sfView_getRotation.argtypes = [View]
cgraphics.sfView_getRotation.restype = ctypes.c_float

cgraphics.sfView_getViewport.argtypes = [View]
cgraphics.sfView_getViewport.restype = FloatRect

cgraphics.sfView_move.argtypes = [View, csfml.system.Vector2f]
cgraphics.sfView_move.restype = None

cgraphics.sfView_rotate.argtypes = [View, ctypes.c_float]
cgraphics.sfView_rotate.restype = None

cgraphics.sfView_zoom.argtypes = [View, ctypes.c_float]
cgraphics.sfView_zoom.restype = None

