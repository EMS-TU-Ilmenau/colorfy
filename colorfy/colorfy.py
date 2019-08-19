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

import json

class Workspace:
    """
    Workspace Class to Handle Everything

    This workspace class is used to handle all Color and ColorMap data in a
    convenient way.
    """
    @property
    def colors(self):
        return self._lstColors

    @property
    def colorMaps(self):
        return self._lstColorMaps

    def __init__(
        self,
        path
    ):
        self._path = path
        try:
            open(self._path + '.json')
        except (FileNotFoundError):
            raise (FileNotFoundError)
        else:
            data_file = open(self._path + '.json')
            self._rawDict = json.load(data_file)

            self._lstColors, self._dictColorNames = self._parseColors(
                self._rawDict['colors']
            )

            self._lstColorMaps = self._parseColorMaps(
                        self._rawDict['colorbars']
                    )

            self._dictFileNames = {
                'CSS': '.css',
                'Python': '.py',
                'TeX': '.tex'
            }

            data_file.close()

    def _parseColors(self, colDict):
        resLst = []
        resDict = {}
        for cc in colDict.items():
            name = cc[0]
            col = Color(cc[1]['def'], name, cc[1]['space'])
            resLst.append(col)
            resDict.update({name: col})

        return (resLst, resDict)

    def _parseColorMaps(self, colDict):
        res = []

        # iterate through all colorbar definitions
        for ccbb in colDict.items():
            lst = []
            name = ccbb[0]
            for cc in ccbb[1]['def']:
                try:
                    lst.append(self._dictColorNames[cc])
                except KeyError:
                    print(
                        "Color " +
                        self._dictColorNames[cc] +
                        " not present in workspace"
                    )

            # we have position keys, then we call the constructor accordingly
            if 'pos' in ccbb[1]:
                res.append(ColorMap(lst, name, ccbb[1]['pos']))
            else:
                res.append(ColorMap(lst, name))

        return res

    def export(self, lstDests, path):

        # iterate through all destination formats and try to write them
        for dd in lstDests:
            try:
                f = open(path + self._dictFileNames[dd], 'w')
            except IOError:
                print(
                    "Could not write to file "
                    + path + self._dictFileNames[dd]
                )
            else:
                # first iterate through and write the colors
                for cc in self._lstColors:
                    f.write(cc.out(dd) + '\n')

                # write colorbars after the colors
                for ccbb in self._lstColorMaps:
                    f.write(ccbb.out(dd) + '\n')

                f.close()


class ColorObject:
    """
    Abstract Colorobject Baseclass
    """

    @property
    def name(self):
        return self._name

    def __init__(
        self,
        name
    ):
        self._name = name

        self._conv2rgb = {
            'rgb': self._eye,
            'cmyk': self._cmyk2rgb,
            'rgb255': self._rgb2552rgb,
        }

        self._rgb2conv = {
            'rgb': self._eye,
            'cmyk': self._rgb2cmyk,
            'rgb255': self._rgb2rgb255,
        }

    def _tplToString(self, tplX):
        """
        converts entries in a tuple to a string and concatenates them with
        commas in between
        """
        return ','.join((str(xx) for xx in tplX))

    """
    conversion functions. rgb is the connecting node in the conversion graph:

    RGB------\        /----RGB
              \      /
    RGB255------RGB--------RGB255
              /      \
    CMYK-----/        \----CMYK
    """

    def _eye(self, *args):
        """
        identity function for convenience
        """
        return tuple(args[0] if len(args) == 1 else args)

    def _cmyk2rgb(self, tplDef):
        c, m, y, k = tplDef
        r = 1.0 - (c + k)
        g = 1.0 - (m + k)
        b = 1.0 - (y + k)
        return (r, g, b)

    def _rgb2552rgb(self, tplDef):
        return tuple(float(cc) / 255.0 for cc in tplDef)

    def _rgb2cmyk(self, tplDef):
        r, g, b = tplDef

        # black
        if (r == 0) and (g == 0) and (b == 0):
            return (0, 0, 0, 1)

        c = 1.0 - r
        m = 1.0 - g
        y = 1.0 - b

        min_cmy = min(c, m, y)
        c = (c - min_cmy)
        m = (m - min_cmy)
        y = (y - min_cmy)
        k = min_cmy

        return tuple(c, m, y, k)

    def _rgb2rgb255(self, tplDef):
        return tuple(int(cc * 255.0) for cc in tplDef)


class Color(ColorObject):

    """
    Class to Represent Colors


    """
    @property
    def tplDef(self):
        return self._tplDef

    def __init__(
        self,
        tplDef,
        name,
        space='rgb'
    ):
        super(Color, self).__init__(name)

        self._tplDef = self._conv2rgb[space](tplDef)

        # dictionary that containts the pattern how to convert a color to a
        # string
        self._dictOutPattern = {
            'CSS': r"""var-%(name)s: %(space)s(%(string)s);""",
            'TeX': r"""\definecolor{%(name)s}{%(space)s}{%(string)s}""",
            'Python': r"""%(name)s = (%(string)s)"""
        }

    def _genOutDict(self, space):
        """
        generalized function to convert color to a dictionary ready for string
        output
        """
        return {
            'name': self._name,
            'space': space,
            'string': self._tplToString(self._conv2rgb[space](self._tplDef))
        }

    def out(self, destination, space='rgb'):
        """
        generalized function to write color in certain space and format
        """
        return self._dictOutPattern[destination] % (
            self._genOutDict(space)
        )


class ColorMap(ColorObject):
    """
    Class to Represent Colorbars


    """
    @property
    def colors(self):
        return self._lstColors

    @property
    def positions(self):
        return self._lstPositions

    def __init__(
        self,
        lstColors,
        name,
        lstPositions=[]
    ):
        super(ColorMap, self).__init__(name)

        # store the list of colors defining this colorbar
        self._lstColors = lstColors

        # if there are positions present, we use them for the definition
        if lstPositions != []:
            self._lstPositions = lstPositions
        else:
            # if not, we place the colors on a regular grid from 0 to 1
            self._lstPositions = list(
                map(
                    lambda x: float(x) / (len(lstColors) - 1),
                    range(len(lstColors))
                )
            )

        # definition syntax in each destination format
        self._outWrapper = {
            'CSS': r"""""",                     # CSS has no colorbars
            'Python': r"""
%(name)s = LinearSegmentedColormap.from_list(
    '%(name)s',
    [%(string)s],
    N=50
)
            """,
            'TeX': r"""\pgfplotsset{
    colormap={%(name)s}{%(string)s},
    colormap/%(name)s/.style={
        colormap name=%(name)s,
    },
}"""
        }

        # how to embed each individual color in the destination syntax
        self._outList = {
            'CSS': r"""""",                     # CSS has no colorbars
            'Python': r"""(%(tpl)s)""",
            'TeX': r"""%(space)s(%(pos)s pt)=(%(tpl)s)"""

        }

        # how are the individual colors separated
        self._outSep = {
            'CSS': r"""""",                     # CSS has no colorbars
            'Python': r""",""",
            'TeX': r""" """
        }

    def out(self, destination, space='rgb'):
        """
        generates a string representing the colorbar in the given
        destination format and the given colorspace
        """

        # list the color information for each color in the colorbar
        lstDicts = [
            {
                'space': space,
                'pos': str(y),
                'tpl': self._tplToString(
                    x._conv2rgb[space](x._tplDef)
                )
            } for x, y in zip(self._lstColors, self._lstPositions)
        ]

        # representing dictionary containing name and string to put
        # into the wrapper string
        dictOut = {
            'name': self._name,
            'string': self._outSep[destination].join(
                self._outList[destination] % (x) for x in lstDicts
            )
        }

        return self._outWrapper[destination] % (dictOut)
