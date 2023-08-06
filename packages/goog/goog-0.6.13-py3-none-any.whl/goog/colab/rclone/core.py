# noinspection PyUnresolvedReferences
from IPython.display import clear_output, HTML
# noinspection PyUnresolvedReferences
from mixlab import checkAvailable, runSh
# noinspection PyUnresolvedReferences
from google.colab import files
# noinspection PyUnresolvedReferences
import ipywidgets as widgets
from subprocess import run
import configparser
import requests
import os
from .utils import _run_command, MakeButton


rclone_conf_path = "/root/.config/rclone"
os.makedirs(rclone_conf_path, exist_ok=True)


def install():
    if not os.path.exists("/usr/bin/rclone"):
        run("curl https://rclone.org/install.sh | sudo bash", shell=True, close_fds=True)


def configure():
    _run_command("rclone config --config {}/rclone.conf".format(rclone_conf_path), False)


def uploadConfig():
    filePath = "{}/rclone.conf".format(rclone_conf_path)
    try:
        if checkAvailable(filePath):
            runSh("rm -f {}".format(filePath))
        uploadedFile = files.upload()
        fileNameDictKeys = uploadedFile.keys()
        fileNo = len(fileNameDictKeys)
        if fileNo == 1:
            for fn in fileNameDictKeys:
                if checkAvailable("/content/{}".format(fn)):
                    runSh("mv -f \"/content/{}\" {}".format(fn, filePath))
                    runSh("chmod 666 {}".format(filePath))
                    runSh("rm -f \"/content/{}\"".format(fn))
                    try:
                        os.remove("/content/upload.txt")
                    except:
                        pass
                    clear_output()
                    print("rclone.conf uploaded 已上传")
        else:
            print("\nNo file is chosen 没有选择文件")
    except:
        print("\nFailed to upload 未能上载")


def uploadRemoteConfig(url, verbose=False):
    filePath = "{}/rclone.conf".format(rclone_conf_path)
    try:
        if checkAvailable(filePath):
            runSh("rm -f {}".format(filePath))
        c = requests.get(url).content
        open(filePath, "wb").write(c)
        runSh("chmod 666 {}".format(filePath))
        try:
            os.remove("/content/upload.txt")
        except:
            pass
        clear_output()
        if verbose:
            print("rclone.conf uploaded 已上传")
    except:
        if verbose:
            print("\nFailed to upload 未能上载")


def downloadConfig():
    filePath = "{}/rclone.conf".format(rclone_conf_path)
    try:
        files.download(filePath)
    except FileNotFoundError:
        print("config file not found 没找到设定文件")


def mountStorage(mountNam, cache_path, verbose=True):
    mPoint = "/mnt/rdrive/{}".format(mountNam)
    try:
        os.makedirs(mPoint)
    except:
        if verbose:
            print("\nfailed to mount 不能挂载 {}\n{} is using 正在使用".format(mountNam, mPoint))
        return
    cmd = ("rclone mount {}: {}".format(mountNam, mPoint) +
           " --config {}/rclone.conf".format(rclone_conf_path) +
           " --user-agent \"Mozilla\"" +
           " --buffer-size 256M" +
           " --transfers 10" +
           " --vfs-cache-mode full" +
           " --vfs-cache-max-age 0h0m1s" +
           " --vfs-cache-poll-interval 0m1s" +
           " --cache-dir {}".format(cache_path) +
           " --allow-other" +
           " --daemon")
    if runSh(cmd, shell=True) == 0:
        if verbose:#rclone mount onedrive_uploaduser1: /mnt/rclone/onedrive_uploaduser1 --network-mode --allow-other --daemon --buffer-size 256M --transfers 10 --cache-dir T:rclone --vfs-cache-mode full --vfs-cache-max-age 0h0m1s --vfs-cache-poll-interval 0m1sr
            print("\nmounted 已挂载 {} on 在 {}".format(mountNam, mPoint))
    else:
        if verbose:
            print("\nfailed to mount 不能挂载 {} on 在 {}".format(mountNam, mPoint))


def unmountStorage(mountNam, verbose=True):
    mPoint = "/mnt/rdrive/{}".format(mountNam)
    if not os.path.exists(mPoint):
        if verbose:
            print("failed to unmount 不能卸载 {} does not exist 不存在".format(mPoint))
        return
    if os.system("fusermount -uz {}".format(mPoint)) == 0:
        runSh("rm -r {}".format(mPoint))
        if verbose:
            print("\nunmounted 已卸载 {} on 在 {}".format(mountNam, mPoint))
    else:
        runSh("fusermount -uz {}".format(mPoint), output=True)


def manageStorage():
    Cache_Directory = "DISK 硬盘（推荐）"  # @param ["RAM 内存", "DISK 硬盘（推荐）"]
    config = configparser.ConfigParser()
    config.read("{}/rclone.conf".format(rclone_conf_path))
    avCon = config.sections()
    mountNam = widgets.Dropdown(options=avCon)
    if Cache_Directory == "RAM 内存":
        cache_path = "/dev/shm"
    elif Cache_Directory == "DISK 硬盘（推荐）":
        os.makedirs("/tmp", exist_ok=True)
        cache_path = "/tmp"
    clear_output(wait=True)
    # noinspection PyUnresolvedReferences
    display(
        widgets.HBox(
            [widgets.VBox(
                [widgets.HTML(
                    '''<h3>connected cloud storage:</h3>'''
                ),
                    mountNam]
            )
            ]
        )
    )
    # noinspection PyUnresolvedReferences
    display(HTML("<br>"), MakeButton("mount 挂载", lambda: mountStorage(mountNam.value, cache_path), "primary"),
            MakeButton("unmount 卸载", lambda: unmountStorage(mountNam.value), "danger"))

