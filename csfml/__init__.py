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

import os
import sys

__all__ = ['module_format', 'graphics']

if sys.platform == 'linux2':
    module_format = 'libcsfml-%s.so'
elif sys.platform == 'win32':
    module_format = 'csfml-%s-2.dll'
else:
    raise NotImplementedError("Don't know how to find CSFML libraries on this platform")

