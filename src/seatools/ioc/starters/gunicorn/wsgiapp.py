from gunicorn.app.wsgiapp import WSGIApplication as GunicornWSGIApplication
from seatools.ioc.config import cfg


class WSGIApplication(GunicornWSGIApplication):

    def init(self, parser, opts, args):
        super().init(parser, opts, args)
        if len(args) > 0:
            # ioc app run
            self.cfg.set('ioc_type', args[0])
            args[0]()
            app =  args[1] if len(args)>1 else  (((cfg().get('seatools') or {}).get('server') or {}).get('gunicorn') or {}).get('app', 'seatools.ioc.server.app:asgi_app')
            self.cfg.set("default_proc_name", app)
            self.app_uri = app

    def load(self):
        if self.cfg.ioc_app is not None:
            self.cfg.ioc_app()
        super().load()


def run(prog=None):
    WSGIApplication("%(prog)s [OPTIONS] [APP_MODULE]", prog=prog).run()


if __name__ == '__main__':
    run()