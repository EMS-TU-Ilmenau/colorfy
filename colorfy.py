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
# along with axify.  If not, see <http://www.gnu.org/licenses/>.

import json
import argparse

parser = argparse.ArgumentParser(
    description=r"""Script that reads color specifications from a JSON
file and exports these definitions consistently in multiple formats."""
)

parser.add_argument(
    '-i',
    action="store",
    help='path to the *.JSON input file without the file extension',
    type=str
)

parser.add_argument(
    '-f',
    action="store",
    help='output formats. [[TeX], Python, CSS]',
    nargs='+',
    default='TeX',
    type=str
)

parser.add_argument(
    '-o',
    action="store",
    help='name of the output file without the file extension',
    type=str
)

args = parser.parse_args()

class Workspace:
    def __init__(
        self,
        path
    ):
        self._path = path
        with open(self._path + '.json') as data_file:
            self._rawDict = json.load(data_file)
        
        self._lstColors, self._dictColorNames= self._parseColors(
                self._rawDict['colors']
                )
        
        self._lstColorBars = self._parseColorBars(self._rawDict['colorbars'])
        
        self._dictFileNames = {
            'CSS': '.css',
            'Python': '.py',
            'TeX': '.tex'
            }
        
    def _parseColors(self, colDict):
        resLst = []
        resDict = {}
        for cc in colDict.items():
            name = cc[0]
            col = Color(cc[1]['def'], name, cc[1]['space'])
            resLst.append(col)
            resDict.update({name : col})
            
        return (resLst, resDict)
    
    def _parseColorBars(self, colDict):
        res = []
        for ccbb in colDict.items():
            lst = []
            name = ccbb[0]
            for cc in ccbb[1]['def']:
                lst.append(self._dictColorNames[cc])
                
            res.append(ColorBar(lst, name))
            
        return res
    
    def export(self, lstDests, path):
        for dd in lstDests:
            f = open(path + self._dictFileNames[dd], 'w')
            for cc in self._lstColors:
                f.write(cc.out(dd) + '\n')
                
            for ccbb in self._lstColorBars:
                f.write(ccbb.out(dd) + '\n')

            f.close()

class ColorObject:
    def __init__(
        self,
        name
    ):

        self._name = name

        self._dictConvFunc = {
            'rgb': self._eye,
            'cmyk': self._rgb2cmyk,
            'rgb255': self._rgb2rgb255,
        }

    def _tplToString(self, tplX):
        return ','.join((str(xx) for xx in tplX))

    def _eye(self, *args):
        if len(args) == 1:
            return args[0]
        return args

    def _cmyk2rgb(self, tplDef):
        pass

    def _rgb2cmyk(self, tplDef):
        pass

    def _rgb2rgb255(self, tplDef):
        pass


class Color(ColorObject):
    def __init__(
        self,
        tplDef,         # defining tuple of the colour
        name,           # color name
        space='rgb'     # color space the color is given in
    ):
        super(Color, self).__init__(name)

        if space == 'rgb':
            self._tplDef = tplDef
        elif space == 'cmyk':
            self._tplDef = cmyk2rgb(tplDef)
        elif space == 'rgb255':
            self._tplDef = (cc / 255.0 for cc in tplDef)
        else:
            self._tplDef = tplDef

        # dictionary that containts the pattern how to convert a color to a
        # string
        self._dictOutPattern = {
            'CSS': r"""var-%(name)s: %(space)s(%(string)s);""",
            'TeX': r"""\definecolor{%(name)s}{%(space)s}{%(string)s}""",
            'Python': r"""%(name)s = (%(string)s)"""
        }

    def _genOutDict(self, space):
        '''
        generalized function to convert color to a dictionary ready for string 
        output
        '''
        return {
            'name': self._name,
            'space': space,
            'string': self._tplToString(self._dictConvFunc[space](self._tplDef))
        }

    def out(self, destination, space='rgb'):
        '''
        generalized function to write color in certain space and format
        '''
        return self._dictOutPattern[destination] % (
            self._genOutDict(space)
        )


class ColorBar(ColorObject):
    def __init__(
        self,
        lstColors,
        name
    ):
        super(ColorBar, self).__init__(name)

        self._lstColors = lstColors

        self._outWrapper = {
            'CSS': r"""""",
            'Python': r"""%(name)s = LinearSegmentedColormap.from_list(
    '%(name)s', 
    [%(string)s], 
    N=50
)
""",
            'TeX': r"""\pgfplotsset{colormap}={%(name)s}{%(string)s}"""
        }

        self._outList = {
            'CSS': r"""""",
            'Python': r"""(%(tpl)s)""",
            'TeX': r"""%(space)s=(%(tpl)s)"""
            
        }

        self._outSep = {
            'CSS': r"""""",
            'Python': r""",""",
            'TeX': r""" """
        }

    def out(self, destination, space='rgb'):
        lstDicts = [
            {
                'space': space,
                'tpl': self._tplToString(
                    x._dictConvFunc[space](x._tplDef)
                )
            } for x in self._lstColors
        ]
        
        dictOut = {
            'name': self._name,
            'string': self._outSep[destination].join(
                self._outList[destination] % (x) for x in lstDicts
                )
            }
        
        return self._outWrapper[destination] % (dictOut)

if __name__ == "__main__":

    # parse arguments
    inPath = args.i
    outputs = args.f
    outPath = args.o
    
    # create the workspace
    w = Workspace(inPath)
    
    # export everything
    w.export(outputs, outPath)
