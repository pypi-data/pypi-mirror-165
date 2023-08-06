import io
import os
import time
import asyncio
import tornado.platform.asyncio
from PIL import ImageGrab
import threading
import tornado.ioloop
import tornado.gen
import tornado.web
import zlib


__ALL__ = ["RemoteScreenServer"]


asyncio.set_event_loop_policy(tornado.platform.asyncio.AnyThreadEventLoopPolicy())


def take_screenshot():
    tmp = io.BytesIO()
    screenshot = ImageGrab.grab()
    screenshot.save(tmp, format="JPEG")
    return tmp.getvalue()


def MainHandler(**kwargs):
    def get(w):
        if w in kwargs:
            return kwargs[w]
        return None
    class _(tornado.web.RequestHandler):
        @tornado.gen.coroutine
        def get(self):
            style = '''<style>
body {
    margin: 0;
    padding: 0;
}
div#screenshot {
    text-align: center;
}
div#screenshot img {
    height: 100%;
}
</style>'''
            script = '''<script>
let img = document.querySelector("div#screenshot img");
img.ondragstart = function() { return false; };
function onmouse(e, d){
    e.preventDefault();
    e.stopPropagation();
    let b = e.which;
    let width = Math.max(
        document.documentElement["clientWidth"],
        document.body["scrollWidth"],
        document.documentElement["scrollWidth"],
        document.body["offsetWidth"],
        document.documentElement["offsetWidth"]
    );
    let height = Math.max(
        document.documentElement["clientHeight"],
        document.body["scrollHeight"],
        document.documentElement["scrollHeight"],
        document.body["offsetHeight"],
        document.documentElement["offsetHeight"]
    );
    let xhr = new XMLHttpRequest();
    let x = e.pageX-img.offsetLeft;
    let y = e.pageY-img.offsetTop;
    xhr.open("GET", "/mouse?xywhdb="+x+","+y+","+img.width+","+img.height+","+d+","+b);
    xhr.send();
}
img.onmouseup = function(e){
    onmouse(e, -1);
}
let moving = 0;
img.onmousemove = function(e){
    if(moving){
        return;
    }
    moving = 1;
    setTimeout(function(){
        moving = 0;
    }, 100);
    onmouse(e, 0);
}
img.onmousedown = function(e){
    onmouse(e, 1);
}
img.onwheel = function(e){
    e.preventDefault();
    e.stopPropagation();
    let d = e.deltaY>0?1:0;
    let xhr = new XMLHttpRequest();
    xhr.open("GET", "/wheel?d="+d);
    xhr.send();
}
function onkey(e, d){
    e.preventDefault();
    e.stopPropagation();
    if(e.keyCode>=65&&e.keyCode<=90){
        let xhr = new XMLHttpRequest();
        xhr.open("GET", "/keys?kd="+String.fromCharCode(e.keyCode+32)+","+d);
        xhr.send();
    }
    else if(e.key){
        let xhr = new XMLHttpRequest();
        xhr.open("GET", "/keys?kd="+e.key+","+d);
        xhr.send();
    }
}
document.onkeyup = function(e){
    onkey(e, 0);
}
document.onkeydown = function(e){
    onkey(e, 1);
}
function get_screenshot() {
    document.querySelector("div#screenshot img").src = "/screenshot?"+(new Date).getTime();
}
setInterval(get_screenshot, 2/3*1000);
</script>'''
            self.write('''{}{}<div id="screenshot"><img/></div>{}{}'''.format(
                style,
                get("extra_headers") or "",
                script,
                get("extra_footers") or "",
            ))

        def check_etag_header(self):
            return False

        def compute_etag(self):
            return None
    return _


def ScreenshotHandler(callback):
    class _(tornado.web.RequestHandler):
        @tornado.gen.coroutine
        def get(self):
            try:
                r = callback(self)
                gzip_compress = zlib.compressobj(9, zlib.DEFLATED, zlib.MAX_WBITS | 16)
                r = gzip_compress.compress(r) + gzip_compress.flush()
                self.set_header("Content-Encoding", 'gzip')
                self.set_header("Content-Length", len(r))
                self.write(r)
            except:
                pass

        def check_etag_header(self):
            return False

        def compute_etag(self):
            return None
    return _


def KMHandler(callback):
    class _(tornado.web.RequestHandler):
        @tornado.gen.coroutine
        def get(self):
            if callable(callback):
                try:
                    callback(self)
                except:
                    pass

        def check_etag_header(self):
            return False

        def compute_etag(self):
            return None
    return _


class ExitHandler(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def get(self):
        self.write('''<script>window.close();</script>''')
        def job():
            time.sleep(1)
            os._exit(0)
        threading.Thread(target=job).start()

    def check_etag_header(self):
        return False

    def compute_etag(self):
        return None


class TemplateHandler(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def job(self):
        ...

    @tornado.gen.coroutine
    def get(self):
        yield self.job()

    def check_etag_header(self):
        return False

    def compute_etag(self):
        return None


def pages_template(
        how_to_take_screenshot=None,
        mouse_callback=None,
        wheel_callback=None,
        keyboard_callback=None,
        extra_handlers=None,
        **kwargs
):
    return [
        (r"/", MainHandler(**kwargs)),
        (r"/screenshot", ScreenshotHandler(how_to_take_screenshot)),
        (r"/mouse", KMHandler(mouse_callback)),
        (r"/wheel", KMHandler(wheel_callback)),
        (r"/keys", KMHandler(keyboard_callback)),
        (r"/stop", ExitHandler),
    ]+(extra_handlers or [])


def make_app(**kwargs):
    return tornado.web.Application(pages_template(**kwargs))


class RemoteScreenServer:
    def __init__(self, port=8888, **kwargs):
        def _():
            self.loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.loop)
            app = make_app(**kwargs)
            app.listen(port)
            tornado.ioloop.IOLoop.current().start()
        p = threading.Thread(target=_)
        p.daemon = True
        p.start()

    def stop(self):
        asyncio.set_event_loop(self.loop)
        tornado.ioloop.IOLoop.current().stop()



