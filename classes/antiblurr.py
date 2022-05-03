"""
ELEKTRON (c) 2022
Written by Matteo Reiter
www.elektron.work
03.05.22 08:08

Calls Win32 API SetProcessDpiAwareness(1) if platform is Win32
to fix potentially blurry windows
"""

# to reslove blurry UI set windows dpi awareness. This will only work
# on windows
import sys
if sys.platform == "win32":
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)