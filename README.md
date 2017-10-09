# colorfy

Managing a pool of colors is very cumbersome, if one wants to use the same 
colors in multiple environments. First color conversion is an issue, if each 
environment works in another color space. Second it should be possible to 
define each color only once in any space available and then provide correct and 
consistent definitions to multiple areas of use, i.e. publications, posters and 
webdesign.

## Features
We are able to read multiple color(bar) definitions from an easily readable 
JSON file, which then is exported to TeX, CSS and Python.

## Usage
To generate the provided example files, one simply calls `python colorfy.py -i 
colors -f TeX CSS Python -o example`.
