import os
from subprocess import run


if not os.path.exists("/root/.ipython/mixlab.py"):
    from shlex import split as _spl

    shellCmd = "wget -qq https://raw.githubusercontent.com/foxe6/MiXLab/master/resources/mixlab.py \
                    -O /root/.ipython/mixlab.py"
    run(_spl(shellCmd))  # nosec


