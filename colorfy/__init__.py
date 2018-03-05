# This file is part of colorfy.

# colorfy is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# colorfy is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with colorfy. If not, see <http://www.gnu.org/licenses/>.


r"""
Colorfy – Handling colors the right way

The entrypoint for any user, who wants to exploit the functionality of
colorfy from within Python, should do the following:

  >>> import colorfy
  >>> ws = colorfy.Workspace('colors.json')

  >>> # access the imported colors as a list
  >>> cols = ws.colors

  >>> # access the imported colormaps as a list
  >>> maps = ws.colorMaps

  >>> # print the first colors definition for TeX in rgb255
  >>> cols[0].out('TeX', 'rgb255')

  >>> # print the first colorbar definition for TeX in rgb
  >>> maps[0].out('TeX', 'rgb')

For further information see the documentation of colorfy.ColorObject,
colorfy.Color, colorfy.ColorMap and colorfy.Workspace.
"""


from .colorfy import Workspace
from .colorfy import ColorObject
from .colorfy import Color
from .colorfy import ColorMap
