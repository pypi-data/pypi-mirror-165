# !/usr/bin/env python
# coding: utf-8
"""
    A command line extension to add snippets directly in Visual Studio Code.

    Author: Fabio Craig Wimmer Florey 
    Copyright: Copyright (C) 2022, Fabio Craig Wimmer Florey.
    All Rights Reserved.

"""
from __future__ import annotations

from argparse import ArgumentParser, BooleanOptionalAction
from json import dumps, loads
from os import getenv, remove

from snippycode.snippySnippets import SnippySnippet
from snippycode.snippyClipboard import snippyClipboard

def snippy():
    parser = ArgumentParser(__doc__)
    parser.add_argument('-l', '--license', action='store_true')

    dict_arguments = {"file": { "commands": ["-f","--file"] ,  "action" : None,  "help": "Script you want to snippy."},
                     "name": {"commands": ["-n","--name"] , "action": None, "help": "Shortcut name of your snippy."}}

    parser.add_argument('-cl', '--clip',
                        action=BooleanOptionalAction,
                        help="Selected text you want to snippy.")
    for i in dict_arguments:
        parser.add_argument(*dict_arguments[i]['commands'],
                            help=dict_arguments[i]['help'])
    arguments = parser.parse_args()

    if arguments.license:
        with open('LICENSE.md','r',encoding='utf-8') as f:
            print('\033[90m'+f.read()+'\033[0m')
    if arguments.file or arguments.clip:
        try:
            JSON_PATH = "/Code/User/snippets/python.json"
            JSON_PATH = f"{getenv('APPDATA')}{JSON_PATH}"

            if CLIPBOARD:= not arguments.file:
                CLIPBOARD = True
                file_path = snippyClipboard()
            else:
                file_path = arguments.file

            snippet = SnippySnippet(file_path, arguments.name).snippet

            if CLIPBOARD:
                remove(file_path)

            with open(JSON_PATH, 'r') as json_file:
                snippet.update(loads(json_file.read()))
            with open(JSON_PATH, 'w') as json_file:
                json_file.write(dumps(snippet, indent=4))
                print('\033[92m - - ---✂'+'┄'*40+' Done!\033[0m')
        
        except Exception as SnippyException:
            print('\033[91m - - ---✂'+'┄'*40+' SnippyException!\033[0m')
            print(SnippyException)

if __name__ == '__main__':
    pass