"""
MIT License

Copyright (c) 2020 Lakhya Jyoti Nath

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

cx freeze setup file for building the game

Version: 1.0.5
Author: Lakhya Jyoti Nath (ljnath)
Email:  ljnath@ljnath.com
Website: https://www.ljnath.com
"""

import sys

from cx_Freeze import Executable, setup

shortcut_metadata = [
    ("DesktopShortcut",                 # Shortcut
     "DesktopFolder",                   # Directory_
     "Play PyBluesky",                  # Name
     "TARGETDIR",                       # Component_
     "[TARGETDIR]pybluesky.exe",        # Target
     None,                              # Arguments
     None,                              # Description
     None,                              # Hotkey
     "",                                # Icon
     None,                              # IconIndex
     False,                             # ShowCmd
     'TARGETDIR'                        # WkDir
    )]


bdist_msi_options= {}
executables =None
if sys.platform == "win32":
    executables = [Executable(
        script="pybluesky.py",
        initScript = None,
        base = "Win32GUI",
        targetName = "pybluesky.exe",
        icon = 'icon/pybluesky.ico'
    )]

    bdist_msi_options = {
        'data': {
            "Shortcut": shortcut_metadata
        },
        'install_icon':'icon/pybluesky.ico'
    }
else:
    executables = [Executable(
        script="pybluesky.py"
    )]


setup(
    name = "PyBluesky",
    version = '1.0.5',
    author = "Lakhya's Innovation Inc.",
    description = 'A simple python game to navigate your jet and fight though a massive missiles attack based on pygame framework',
    executables = executables,
    options={
        "bdist_msi": bdist_msi_options,
        "build_exe": {
            "optimize" : 2,
            "packages":[
                "pygame",
                "asyncio",
                "aiohttp"
            ],
            "includes":[
                'math',
                'random'
            ],
            "include_files": [
                'audio/',
                'font/',
                'image/',
                'icon/',
                'LICENSE'
            ]
        }
    }
)
