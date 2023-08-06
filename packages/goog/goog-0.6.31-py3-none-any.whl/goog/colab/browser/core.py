from omnitools import abs_dir
from ..utils import runShell
import os


def startWebkit(sc_port):
    t = open(os.path.join(abs_dir(__file__), "webkit.py"), "rb").read().decode()
    t = t.replace("'<sc_port>'", str(sc_port))
    open("webkit.py", "wb").write(t.encode())
    runShell("python3.7 webkit.py")

