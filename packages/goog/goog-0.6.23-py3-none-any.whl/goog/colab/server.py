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


def startRSS(port, sc_port):
    t = '''
    from remotescreen import RemoteScreenServer, TemplateHandler
    from unencryptedsocket import SC
    import tornado.web
    import tornado.gen
    import json
    import time
    def sc():
        return SC(host="127.0.0.1", port=sc_port)
    def add_job(t, v):
        return sc().request(command="add_job", data=((t, v), {}))
    def get_job_result(t):
        r = sc().request(command="get_job_result", data=((t,), {}))
        if isinstance(r, Exception):
            raise KeyError
        return r
    def get_tabs(*args, **kwargs):
        return sc().request(command="get_tabs", data=(args, kwargs))
    def set_tab(*args, **kwargs):
        return sc().request(command="set_tab", data=(args, kwargs))
    def close_tab(*args, **kwargs):
        return sc().request(command="close_tab", data=(args, kwargs))
    def screenshot(
            self  # type: tornado.web.RequestHandler
    ):
        t = time.time()
        # jobs[t] = (["screenshot"])
        add_job(t, ["screenshot"])
        elapsed = 0
        while elapsed <= 1:
            try:
                # return job_results.pop(t)
                return get_job_result(t)
            except:
                time.sleep(1/1000)
                elapsed += 1/1000
        return "timeout"
    def mouse_cb(
            self  # type: tornado.web.RequestHandler
    ):
        args = list(map(int, self.get_argument("xywhdb").split(",")))
        t = time.time()
        # jobs[t] = (["mouse", *args])
        add_job(t, ["mouse", *args])
        elapsed = 0
        while elapsed <= 1:
            try:
                # return job_results.pop(t)
                return get_job_result(t)
            except:
                time.sleep(1/1000)
                elapsed += 1/1000
        return "timeout"
    def wheel_cb(
            self  # type: tornado.web.RequestHandler
    ):
        args = [int(self.get_argument("d"))]
        t = time.time()
        # jobs[t] = (["wheel", *args])
        add_job(t, ["wheel", *args])
        elapsed = 0
        while elapsed <= 1:
            try:
                # return job_results.pop(t)
                return get_job_result(t)
            except:
                time.sleep(1/1000)
                elapsed += 1/1000
        return "timeout"
    def keyboard_cb(
            self  # type: tornado.web.RequestHandler
    ):
        args = self.get_argument("kd", strip=False).split(",")
        args[1] = int(args[1])
        t = time.time()
        # jobs[t] = (["keyboard", *args])
        add_job(t, ["keyboard", *args])
        elapsed = 0
        while elapsed <= 1:
            try:
                # return job_results.pop(t)
                return get_job_result(t)
            except:
                time.sleep(1/1000)
                elapsed += 1/1000
        return "timeout"
    class GetTabsHandler(TemplateHandler):
        @tornado.gen.coroutine
        def job(self):
            self.write(json.dumps(get_tabs()))
    class SetTabHandler(TemplateHandler):
        @tornado.gen.coroutine
        def job(self):
            set_tab(int(self.get_argument("id")))
    class CloseTabHandler(TemplateHandler):
        @tornado.gen.coroutine
        def job(self):
            close_tab(int(self.get_argument("id")))
    class TestHandler(TemplateHandler):
        @tornado.gen.coroutine
        def job(self):
            self.write("ok")
    RemoteScreenServer(
        port=<port>,
        how_to_take_screenshot=screenshot,
        mouse_callback=mouse_cb,
        wheel_callback=wheel_cb,
        keyboard_callback=keyboard_cb,
        extra_handlers=[
            (r"/get_tabs", GetTabsHandler),
            (r"/set_tab", SetTabHandler),
            (r"/close_tab", CloseTabHandler),
            (r"/test", TestHandler),
        ],
        extra_headers=\'''
<style>
body{
    color: white;
    font-family: "Trebuchet MS", san-serif;
    background-color: black;
}
div#screenshot img {
    height: calc(100% - 30px);
}
div#tabs{
    display: flex;
    justify-content: center;
    align-items: center;
}
div#tabs div[id]{
    padding: 5px 10px;
    border-right: 1px solid white;
    cursor: pointer;
    letter-spacing: -1px;
}
div#tabs div[id]:first-child{
    border-left: 1px solid white;
}
</style>
<div id="tabs"></div>
\''',
        extra_footers=\'''<script>
setInterval(function(){
    let xhr = new XMLHttpRequest();
    xhr.onload = function(){
        document.querySelector("div#tabs").innerHTML = "";
        let tabs = JSON.parse(this.responseText);
        for(let t of tabs){
            let tab = document.createElement("div");
            tab.id = t[0];
            tab.innerHTML = t[1]+" <span class='close'>[x]</span>";
            tab.onclick = function(e){
                let xhr = new XMLHttpRequest();
                xhr.open("GET", "/set_tab?id="+e.target.id);
                xhr.send();
            }
            document.querySelector("div#tabs").appendChild(tab);
        }
        Array.from(document.querySelectorAll("div#tabs span.close")).map(function(e){
            e.addEventListener("click", function(e){
                e.preventDefault();
                e.stopPropagation();
                let xhr = new XMLHttpRequest();
                xhr.open("GET", "/close_tab?id="+e.target.parentElement.id);
                xhr.send();
            });
        });
    }
    xhr.open("GET", "/get_tabs");
    xhr.send();
}, 1000);
</script>\''',
    )
'''.replace("<port>", str(port))
    open("rss.py", "wb").write(t.encode())
    runSh("python3.7 rss.py", shell=True)


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

