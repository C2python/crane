import copy
from distutils import spawn
import math
import os
import sys

from crane import service
from crane import app
from crane import opts
from crane import utils
from oslo_config import cfg
from oslo_log import log as logging

LOG = logging.getLogger(__name__)


def build_wsgi_app(argv=None):
    return app.load_app(service.prepare_service(args=argv))

def api():
    # Compat with previous pbr script
    try:
        double_dash = sys.argv.index("--")
    except ValueError:
        double_dash = None
    else:
        sys.argv.pop(double_dash)

    conf = cfg.ConfigOpts()

    '''for opt in opts.api_opts:
        cp = copy.copy(opt)
        cp.default = None
        conf.register_cli_opt(cp)
    '''
    conf = service.prepare_service(conf)

    if double_dash is not None:
        # NOTE(jd) Wait to this stage to log so we're sure the logging system
        # is in place
        LOG.warning(
            "No need to pass `--' in gnocchi-api command line anymore, "
            "please remove")

    uwsgi = spawn.find_executable("uwsgi")
    if not uwsgi:
        LOG.error("Unable to find `uwsgi'.\n"
                  "Be sure it is installed and in $PATH.")
        return 1

    workers = utils.get_default_workers()

    args = [
        "--if-not-plugin", "python", "--plugin", "python", "--endif",
        "--%s" % conf.api.uwsgi_mode, "%s:%d" % (
            conf.host or conf.api.host,
            conf.port or conf.api.port),
        "--master",
        "--enable-threads",
        "--thunder-lock",
        "--hook-master-start", "unix_signal:15 gracefully_kill_them_all",
        "--die-on-term",
        "--processes", str(math.floor(workers * 1.5)),
        "--threads", str(workers),
        "--lazy-apps",
        "--chdir", "/",
        "--wsgi", "crane.wsgi",
        "--pyargv", " ".join(sys.argv[1:]),
    ]
    if conf.api.uwsgi_mode == "http":
        args.extend([
            "--so-keepalive",
            "--http-keepalive",
            "--add-header", "Connection: Keep-Alive"
        ])

    virtual_env = os.getenv("VIRTUAL_ENV")
    if virtual_env is not None:
        args.extend(["-H", os.getenv("VIRTUAL_ENV", ".")])

    return os.execl(uwsgi, uwsgi, *args)

