# noinspection PyUnresolvedReferences
import codecs, contextlib, locale, os, pty, select, signal, subprocess, sys, termios, time
# noinspection PyUnresolvedReferences
from IPython.display import clear_output, HTML, clear_output
# noinspection PyUnresolvedReferences
from google.colab import _ipython, _message, files, output
# noinspection PyUnresolvedReferences
from google.colab.output import _tags
# noinspection PyUnresolvedReferences
from IPython.utils import text
# noinspection PyUnresolvedReferences
import ipywidgets as widgets
from subprocess import run
import configparser
import requests
import uuid
import six
import os
import re


__ALL__ = [
    "rclone_conf_path", "mixlab",
    "install", "configure",
    "uploadConfig", "downloadConfig", "uploadRemoteConfig",
    "mountStorage", "unmountStorage", "manageStorage"
]


_PTY_READ_MAX_BYTES_FOR_TEST = 2 ** 20  # 1MB
_ENCODING = "UTF-8"
rclone_conf_path = "/root/.config/rclone"
os.makedirs(rclone_conf_path, exist_ok=True)
if not os.path.exists("/root/.ipython/mixlab.py"):
    from shlex import split as _spl

    shellCmd = "wget -qq https://raw.githubusercontent.com/foxe6/MiXLab/master/resources/mixlab.py \
                    -O /root/.ipython/mixlab.py"
    run(_spl(shellCmd))  # nosec

# noinspection PyUnresolvedReferences
from mixlab import checkAvailable, runSh


def install():
    if not os.path.exists("/usr/bin/rclone"):
        run("curl https://rclone.org/install.sh | sudo bash", shell=True, close_fds=True)


class ShellResult(object):
    """Result of an invocation of the shell magic.

    Note: This is intended to mimic subprocess.CompletedProcess, but has slightly
    different characteristics, including:
      * CompletedProcess has separate stdout/stderr properties. A ShellResult
        has a single property containing the merged stdout/stderr stream,
        providing compatibility with the existing "!" shell magic (which this is
        intended to provide an alternative to).
      * A custom __repr__ method that returns output. When the magic is invoked as
        the only statement in the cell, Python prints the string representation by
        default. The existing "!" shell magic also returns output.
    """

    def __init__(self, args, returncode, command_output):
        self.args = args
        self.returncode = returncode
        self.output = command_output

    def check_returncode(self):
        if self.returncode:
            raise subprocess.CalledProcessError(
                returncode=self.returncode, cmd=self.args, output=self.output)

    def _repr_pretty_(self, p, cycle):  # pylint:disable=unused-argument
        # Note: When invoking the magic and not assigning the result
        # (e.g. %shell echo "foo"), Python's default semantics will be used and
        # print the string representation of the object. By default, this will
        # display the __repr__ of ShellResult. Suppress this representation since
        # the output of the command has already been displayed to the output window.
        if cycle:
            raise NotImplementedError


def _configure_term_settings(pty_fd):
    term_settings = termios.tcgetattr(pty_fd)
    # ONLCR transforms NL to CR-NL, which is undesirable. Ensure this is disabled.
    # http://man7.org/linux/man-pages/man3/termios.3.html
    term_settings[1] &= ~termios.ONLCR

    # ECHOCTL echoes control characters, which is undesirable.
    term_settings[3] &= ~termios.ECHOCTL

    termios.tcsetattr(pty_fd, termios.TCSANOW, term_settings)


def _run_command(cmd, clear_streamed_output):
    """Calls the shell command, forwarding input received on the stdin_socket."""
    locale_encoding = locale.getpreferredencoding()
    if locale_encoding != _ENCODING:
        raise NotImplementedError(
            "A UTF-8 locale is required. Got {}".format(locale_encoding))

    parent_pty, child_pty = pty.openpty()
    _configure_term_settings(child_pty)

    epoll = select.epoll()
    epoll.register(
        parent_pty,
        (select.EPOLLIN | select.EPOLLOUT | select.EPOLLHUP | select.EPOLLERR))

    try:
        temporary_clearer = _tags.temporary if clear_streamed_output else _no_op

        with temporary_clearer(), _display_stdin_widget(
                delay_millis=500) as update_stdin_widget:
            # TODO(b/115531839): Ensure that subprocesses are terminated upon
            # interrupt.
            p = subprocess.Popen(
                cmd,
                shell=True,
                executable="/bin/bash",
                stdout=child_pty,
                stdin=child_pty,
                stderr=child_pty,
                close_fds=True)
            # The child PTY is only needed by the spawned process.
            os.close(child_pty)

            return _monitor_process(parent_pty, epoll, p, cmd, update_stdin_widget)
    finally:
        epoll.close()
        os.close(parent_pty)


class _MonitorProcessState(object):

    def __init__(self):
        self.process_output = six.StringIO()
        self.is_pty_still_connected = True


def _monitor_process(parent_pty, epoll, p, cmd, update_stdin_widget):
    """Monitors the given subprocess until it terminates."""
    state = _MonitorProcessState()

    # A single UTF-8 character can span multiple bytes. os.read returns bytes and
    # could return a partial byte sequence for a UTF-8 character. Using an
    # incremental decoder is incrementally fed input bytes and emits UTF-8
    # characters.
    decoder = codecs.getincrementaldecoder(_ENCODING)()

    num_interrupts = 0
    echo_status = None
    while True:
        try:
            result = _poll_process(parent_pty, epoll, p, cmd, decoder, state)
            if result is not None:
                return result
            term_settings = termios.tcgetattr(parent_pty)
            new_echo_status = bool(term_settings[3] & termios.ECHO)
            if echo_status != new_echo_status:
                update_stdin_widget(new_echo_status)
                echo_status = new_echo_status
        except KeyboardInterrupt:
            try:
                num_interrupts += 1
                if num_interrupts == 1:
                    p.send_signal(signal.SIGINT)
                elif num_interrupts == 2:
                    # Process isn't responding to SIGINT and user requested another
                    # interrupt. Attempt to send SIGTERM followed by a SIGKILL if the
                    # process doesn't respond.
                    p.send_signal(signal.SIGTERM)
                    time.sleep(0.5)
                    if p.poll() is None:
                        p.send_signal(signal.SIGKILL)
            except KeyboardInterrupt:
                # Any interrupts that occur during shutdown should not propagate.
                pass

            if num_interrupts > 2:
                # In practice, this shouldn't be possible since
                # SIGKILL is quite effective.
                raise


def _poll_process(parent_pty, epoll, p, cmd, decoder, state):
    """Polls the process and captures / forwards input and output."""

    terminated = p.poll() is not None
    if terminated:
        termios.tcdrain(parent_pty)
        # We're no longer interested in write events and only want to consume any
        # remaining output from the terminated process. Continuing to watch write
        # events may cause early termination of the loop if no output was
        # available but the pty was ready for writing.
        epoll.modify(parent_pty,
                     (select.EPOLLIN | select.EPOLLHUP | select.EPOLLERR))

    output_available = False

    events = epoll.poll()
    input_events = []
    for _, event in events:
        if event & select.EPOLLIN:
            output_available = True
            raw_contents = os.read(parent_pty, _PTY_READ_MAX_BYTES_FOR_TEST)
            # import re
            # decoded_contents = re.sub(r"http:\/\/127.0.0.1:53682", Server["url"],
            #                          decoder.decode(raw_contents))
            decoded_contents = decoder.decode(raw_contents)
            sys.stdout.write(decoded_contents)
            state.process_output.write(decoded_contents)

        if event & select.EPOLLOUT:
            # Queue polling for inputs behind processing output events.
            input_events.append(event)

        # PTY was disconnected or encountered a connection error. In either case,
        # no new output should be made available.
        if (event & select.EPOLLHUP) or (event & select.EPOLLERR):
            state.is_pty_still_connected = False

    for event in input_events:
        # Check to see if there is any input on the stdin socket.
        # pylint: disable=protected-access
        input_line = _message._read_stdin_message()
        # pylint: enable=protected-access
        if input_line is not None:
            # If a very large input or sequence of inputs is available, it's
            # possible that the PTY buffer could be filled and this write call
            # would block. To work around this, non-blocking writes and keeping
            # a list of to-be-written inputs could be used. Empirically, the
            # buffer limit is ~12K, which shouldn't be a problem in most
            # scenarios. As such, optimizing for simplicity.
            input_bytes = bytes(input_line.encode(_ENCODING))
            os.write(parent_pty, input_bytes)

    # Once the process is terminated, there still may be output to be read from
    # the PTY. Wait until the PTY has been disconnected and no more data is
    # available for read. Simply waiting for disconnect may be insufficient if
    # there is more data made available on the PTY than we consume in a single
    # read call.
    if terminated and not state.is_pty_still_connected and not output_available:
        sys.stdout.flush()
        command_output = state.process_output.getvalue()
        return ShellResult(cmd, p.returncode, command_output)

    if not output_available:
        # The PTY is almost continuously available for reading input to provide
        # to the underlying subprocess. This means that the polling loop could
        # effectively become a tight loop and use a large amount of CPU. Add a
        # slight delay to give resources back to the system while monitoring the
        # process.
        # Skip this delay if we read output in the previous loop so that a partial
        # read doesn't unnecessarily sleep before reading more output.
        # TODO(b/115527726): Rather than sleep, poll for incoming messages from
        # the frontend in the same poll as for the output.
        time.sleep(0.1)


@contextlib.contextmanager
def _display_stdin_widget(delay_millis=0):
    """Context manager that displays a stdin UI widget and hides it upon exit.

    Args:
      delay_millis: Duration (in milliseconds) to delay showing the widget within
        the UI.

    Yields:
      A callback that can be invoked with a single argument indicating whether
      echo is enabled.
    """
    shell = _ipython.get_ipython()
    display_args = ["cell_display_stdin", {"delayMillis": delay_millis}]
    _message.blocking_request(*display_args, parent=shell.parent_header)

    def echo_updater(new_echo_status):
        # Note: Updating the echo status uses colab_request / colab_reply on the
        # stdin socket. Input provided by the user also sends messages on this
        # socket. If user input is provided while the blocking_request call is still
        # waiting for a colab_reply, the input will be dropped per
        # https://github.com/googlecolab/colabtools/blob/56e4dbec7c4fa09fad51b60feb5c786c69d688c6/google/colab/_message.py#L100.
        update_args = ["cell_update_stdin", {"echo": new_echo_status}]
        _message.blocking_request(*update_args, parent=shell.parent_header)

    yield echo_updater

    hide_args = ["cell_remove_stdin", {}]
    _message.blocking_request(*hide_args, parent=shell.parent_header)


@contextlib.contextmanager
def _no_op():
    yield


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


class MakeButton(object):
    def __init__(self, title, callback, style):
        self._title = title
        self._callback = callback
        self._style = style

    def _repr_html_(self):
        callback_id = "button-" + str(uuid.uuid4())
        output.register_callback(callback_id, self._callback)
        if self._style != "":
            style_html = "p-Widget jupyter-widgets jupyter-button widget-button mod-" + self._style
        else:
            style_html = "p-Widget jupyter-widgets jupyter-button widget-button"
        template = """<button class="{style_html}" id="{callback_id}">{title}</button>
        <script>
          document.querySelector("#{callback_id}").onclick = (e) => {{
            google.colab.kernel.invokeFunction("{callback_id}", [], {{}})
            e.preventDefault();
          }};
        </script>"""
        html = template.format(title=self._title, callback_id=callback_id, style_html=style_html)
        return html


def ShowAC(mountNam, cache_path):
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
        if verbose:
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
    ShowAC(mountNam, cache_path)

