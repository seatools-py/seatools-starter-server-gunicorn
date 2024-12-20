import importlib

from gunicorn.app.wsgiapp import WSGIApplication as GunicornWSGIApplication
from gunicorn.config import Setting, validate_string
from seatools.ioc.config import cfg


class WSGIApplication(GunicornWSGIApplication):

    def init(self, parser, opts, args):
        super().init(parser, opts, args)
        if len(args) > 0:
            # ioc app run
            ioc_app_path = args[0]
            module_name, func_name = ioc_app_path.split(':')
            self.ioc_app = getattr(importlib.import_module(module_name), func_name)
            self.ioc_app()
            app =  args[1] if len(args)>1 else  (((cfg().get('seatools') or {}).get('server') or {}).get('gunicorn') or {}).get('app', 'seatools.ioc.server.app:wsgi_app')
            print("gunicorn app:", app)
            self.cfg.set("default_proc_name", app)
            self.app_uri = app

    def load(self):
        if hasattr(self, 'ioc_app'):
            self.ioc_app()
        super().load()


class IocAppSetting(Setting):
    name = "ioc_app"
    section = "Seatools IOC Start APP"
    meta = "String"
    validator = validate_string
    default = None
    desc = """\
        A Seatools start function path in pattern ``$(MODULE_NAME):$(FUNCTION_NAME)``.

        """


def run(prog=None):
    WSGIApplication("%(prog)s [OPTIONS] [APP_MODULE]", prog=prog).run()


if __name__ == '__main__':
    run()
