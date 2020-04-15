from pecan import make_app
import os
import pkg_resources
import uuid

from oslo_log import log as logging
from paste import deploy
import pecan
from stevedore import driver

LOG = logging.getLogger(__name__)

global APPCONFIGS
APPCONFIGS = {}



def load_app(conf):
    global APPCONFIGS

    # Build the WSGI app
    cfg_path = conf.api.paste_config
    if not os.path.isabs(cfg_path):
        cfg_path = conf.find_file(cfg_path)

    if cfg_path is None or not os.path.exists(cfg_path):
        LOG.debug("No api-paste configuration file found! Using default.")
        cfg_path = os.path.abspath(pkg_resources.resource_filename(
            __name__, "api-paste.ini"))

    config = dict(conf=conf)
    configkey = str(uuid.uuid4())
    APPCONFIGS[configkey] = config

    LOG.info("WSGI config used: %s", cfg_path)

    appname = "crane+basic"
    return deploy.loadapp("config:" + cfg_path, name=appname,
                         global_conf={'configkey': configkey})

def _setup_app(root,conf):

    app = pecan.make_app(
        root,
        guess_content_type_from_ext=False
    )
    return app


def app_factory(global_config, **local_conf):
    global APPCONFIGS
    appconfig = APPCONFIGS.get(global_config.get('configkey'))
    return _setup_app(root=local_conf.get('root'), **appconfig)