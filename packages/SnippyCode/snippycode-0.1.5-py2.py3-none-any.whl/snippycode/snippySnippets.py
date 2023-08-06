# !/usr/bin/env python
# coding: utf-8
"""
SnippySnippet:
    JSON representation of a SnippyObject
"""
from __future__ import annotations

from dataclasses import dataclass
from json import dumps, loads

from snippycode.snippyObjects import PythonSnippy

@dataclass
class SnippySnippet:
    '''
    Snippet class of a given file
    '''
    path: str
    prefix: str
    
    def __post_init__(self):
        file_to_snippify = PythonSnippy(self.path)
        self.body = file_to_snippify.body
        self.description = file_to_snippify.description
        del self.path
        self.snippet = loads("{"+ 
                        f'"snippy-code_{self.prefix}"'+ 
                        f":{dumps(self.__dict__, indent=4)}" + "}")
                        
if __name__ == '__main__':
    pass