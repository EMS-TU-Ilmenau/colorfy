# colorfy

Managing a pool of colors is very cumbersome, if one wants to use the same
colors in multiple environments. First color conversion is an issue, if each
environment works in another color space. Second it should be possible to
define each color only once in any space available and then provide correct and
consistent definitions to multiple areas of use, i.e. publications, posters and
webdesign.

## Features
We are able to read multiple color and colormap definitions from an easily
readable JSON file, which then is exported to TeX, CSS and Python.

## Installation
If you want to use colorfy as a module, then call 'pip install .' from this
git repository after cloning. This is neccessary, if you use other tools
that depend on colorfy.

## Usage
Although colorfy provides access from Python as a module, it should be used
as a command line tool for the highest convenience.

Suppose you are given a JSON file called 'colors.json' and you want to export
all colors and colormaps in this file to TeX, CSS and Python, then you should
call the following command:

`python colorfy.py -p colors -f TeX CSS Python -o example`

This will create the files `example.{css,py,tex}` with the respective color
definitions ready to use in the respective language.
