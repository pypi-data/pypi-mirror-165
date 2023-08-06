import io
import os
import time
from PIL import ImageGrab
import threading
import tornado.ioloop
import tornado.gen
import tornado.web


__ALL__ = ["RemoteScreenServer"]


def take_screenshot():
    tmp = io.BytesIO()
    screenshot = ImageGrab.grab()
    screenshot.save(tmp, format="JPEG")
    return tmp.getvalue()


class MainHandler(tornado.web.RequestHandler):
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
function onmouse(e, w){
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
    var xhr = new XMLHttpRequest();
    xhr.open("GET", "/mouse?xywhs="+e.pageX+","+e.pageY+","+width+","+height+","+w);
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
    let d = e.deltaY>0?1:0;
    var xhr = new XMLHttpRequest();
    xhr.open("GET", "/wheel?d="+d);
    xhr.send();
}
function onkey(e, w){
    if(e.keyCode>=65&&e.keyCode<=90){
        var xhr = new XMLHttpRequest();
        xhr.open("GET", "/keys?ks="+String.fromCharCode(e.keyCode+32)+","+w);
        xhr.send();
    }
    else if(e.key){
        var xhr = new XMLHttpRequest();
        xhr.open("GET", "/keys?ks="+e.key+","+w);
        xhr.send();
    }
}
document.onkeyup = function(e){
    e.preventDefault();
    e.stopPropagation();
    onkey(e, 0);
}
document.onkeydown = function(e){
    e.preventDefault();
    e.stopPropagation();
    onkey(e, 1);
}
function get_screenshot() {
    document.querySelector("div#screenshot img").src = "/screenshot?"+(new Date).getTime();
}
setInterval(get_screenshot, 2/3*1000);
</script>'''
        self.write('''{}<div id="screenshot"><img/></div>{}'''.format(style, script))

    def check_etag_header(self):
        return False

    def compute_etag(self):
        return None


def ScreenshotHandler(how_to_take_screenshot):
    class _(tornado.web.RequestHandler):
        @tornado.gen.coroutine
        def get(self):
            self.write(how_to_take_screenshot())

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


def pages_template(how_to_take_screenshot=None, mouse_callback=None, wheel_callback=None, keyboard_callback=None):
    return [
        (r"/", MainHandler),
        (r"/screenshot", ScreenshotHandler(how_to_take_screenshot)),
        (r"/mouse", KMHandler(mouse_callback)),
        (r"/wheel", KMHandler(wheel_callback)),
        (r"/keys", KMHandler(keyboard_callback)),
        (r"/stop", ExitHandler),
    ]


def make_app(**kwargs):
    return tornado.web.Application(pages_template(**kwargs))


def RemoteScreenServer(**kwargs):
    app = make_app(**kwargs)
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()



