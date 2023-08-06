# noinspection PyUnresolvedReferences
from mixlab import runSh, PortForward_wrapper
# noinspection PyUnresolvedReferences
from IPython.display import clear_output
from urllib.parse import urlparse
import urllib.request


def startFileServer(port, cd="/"):
    try:
        urllib.request.urlopen("http://localhost:{}".format(port))
        return False
    except:
        runSh("python3.7 -m http.server {} &".format(port), shell=True, cd=cd)
        return True


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
    data = Server.start(name, displayB=False)
    clear_output()
    return urlparse(data['url'])._replace(scheme='https').geturl()

