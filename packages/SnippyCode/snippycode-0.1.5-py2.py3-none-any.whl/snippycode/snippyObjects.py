# !/usr/bin/env python
# coding: utf-8

"""
SnyppyObjects:
    Scripts that you want to turn into snippets.
"""
from __future__ import annotations

from ast import get_docstring, parse
from dataclasses import dataclass
from pathlib import Path

class ExtensionError(Exception):
    """
    Exception raised for untested extensions.
    """
    def __init__(self) -> None:
        super().__init__('Snippy only accepts .py and .tmp files')

@dataclass
class PythonSnippy:
    path: str
    
    def __post_init__(self)-> PythonSnippy:
        # FIXME: for now, it will work with .py files and .tmp files only,
        # in the future I plan to create a Snippy object and  specific objects 
        # that extend the SnippyObject  (ideally outside of the python scope)
        # posting outside the python json.
        encoding = 'utf-8'
        extensions = {
                        "Python": [".py"] ,
                        "Temp"  : [".tmp"]
                        }
        _extension = Path(self.path).suffix
        with open(self.path, 'r', encoding=encoding) as f:
            _body = f.read()
        if _extension in extensions['Python']:
            module = parse(_body)
            self.description = get_docstring(module)
            self.body = _body
            return self
        elif _extension in extensions['Temp']:
            self.description = "Snippy for the clipboard."
            self.body = _body
        else:
            raise ExtensionError

if __name__ == '__main__':
    pass