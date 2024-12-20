import importlib

from gunicorn.app.wsgiapp import Application
from gunicorn.config import Setting, validate_string
from seatools.ioc.config import cfg


class WSGIApplication(Application):
    """seatools.ioc WSGIApplication."""

    def init(self, parser, opts, args):
        if len(args) > 0:
            # ioc app run
            ioc_app_path = args[0]
            module_name, func_name = ioc_app_path.split(':')
            self.ioc_app = getattr(importlib.import_module(module_name), func_name)
            self.ioc_app()
            config = (((cfg().get('seatools') or {}).get('server') or {}).get('gunicorn') or {})
            if not isinstance(config, dict):
                config = {}
            self.app_factory_path = config.get('app', 'seatools.ioc.server.app:wsgi_app')
            if len(args) > 1:
                self.app_factory_path = args[1]
            # server config override
            for k, v in config.items():
                if k != 'app':
                    self.cfg.set(k, v)
    
    def load_wsgiapp(self):
        module_name, func_name = self.app_factory_path.split(":")
        return getattr(importlib.import_module(module_name), func_name)()
                
    def load(self):
        self.ioc_app()
        return self.load_wsgiapp()


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
