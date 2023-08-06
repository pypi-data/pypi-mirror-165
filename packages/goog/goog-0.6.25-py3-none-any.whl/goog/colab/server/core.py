# noinspection PyUnresolvedReferences
from mixlab import runSh, PortForward_wrapper
# noinspection PyUnresolvedReferences
from IPython.display import clear_output
from urllib.parse import urlparse
from ..utils import runShell
import urllib.request
import os


def startFileServer(port, cd="/"):
    try:
        urllib.request.urlopen("http://localhost:{}".format(port))
        return False
    except:
        runShell("python3.7 -m http.server {}".format(port), shell=True, cd=cd)
        return True


def startRSS(port, sc_port):
    t = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "rss.py"), "rb").read().decode()
    t = t.replace("'<port>'", str(port)).replace("'<sc_port>'", str(sc_port))
    open("rss.py", "wb").write(t.encode())
    runShell("python3.7 rss.py")


def penetrateIntranet(name, port):
    PORT_FORWARD = "argotunnel"
    TOKEN = ""
    USE_FREE_TOKEN = True
    REGION = "JP"
    Server = PortForward_wrapper(
        PORT_FORWARD,
        TOKEN,
        USE_FREE_TOKEN,
        [[name, port, 'http']],
        REGION.lower(),
        ["", 5042]
    )
    data = Server.start(name, displayB=False, v=False)
    return urlparse(data['url'])._replace(scheme='https').geturl()

