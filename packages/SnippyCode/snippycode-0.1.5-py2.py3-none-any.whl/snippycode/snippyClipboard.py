# !/usr/bin/env python
# coding: utf-8

"""
SnippyClipboard:
    This script creates a temporary file from a clipboard selection.
"""
from __future__ import annotations

import ctypes
from os import getenv

def snippyClipboard() -> str | None:
        """
        This function returns the clipboard on Windows.

        I shamelessly stole this code from StackOverFlow:
            https://stackoverflow.com/a/23285159

        """
        # TODO: I tested it on a Windows 11 Home with Python 3.10.6 64-bit
        #      It works flawlessly, althought some comments point out that it might
        #      not work with other version, in the next updates, I'll check.
       
        # TODO: It works on Windows only, but I wanted to keep Snippy as close
        #       to the Standard Library as possibile. I might add UNIX
        #      functionalities in the future,  if the project gains traction.

        # TODO: This code is kinda messy and needs refactoring.

        CF_TEXT = 1
        ENCODING = 'utf-8'

        kernel32 = ctypes.windll.kernel32
        kernel32.GlobalLock.argtypes = [ctypes.c_void_p]
        kernel32.GlobalLock.restype = ctypes.c_void_p
        kernel32.GlobalUnlock.argtypes = [ctypes.c_void_p]
        user32 = ctypes.windll.user32
        user32.GetClipboardData.restype = ctypes.c_void_p

        def get_clipboard_text() -> str:
            user32.OpenClipboard(0)
            try:
                if user32.IsClipboardFormatAvailable(CF_TEXT):
                    data = user32.GetClipboardData(CF_TEXT)
                    data_locked = kernel32.GlobalLock(data)
                    text = ctypes.c_char_p(data_locked)
                    value = text.value
                    kernel32.GlobalUnlock(data_locked)
                    return value.decode(ENCODING)
            finally:
                user32.CloseClipboard()
        
        def write_file():
            """
            Create a temporary `.tmp` file in the directory.
            """
            clipboard = get_clipboard_text()
            try:
                file_path = f"{getenv('TEMP')}/snippyclip.tmp"
                with open(file_path,'w',encoding=ENCODING) as f:
                    f.write(clipboard)
                    return file_path
            except Exception:
                pass

        return write_file()

if __name__ == '__main__':
    pass