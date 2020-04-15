from oslo_log import log
from crane import opts
from oslo_config import cfg

def prepare_service(argv=None,config_file=None):
    conf = cfg.ConfigOpts()
    opts.add_opts()
    #opts.add_cli_opts()
    log.register_options(conf)
    log.setup(conf,'crane')
    return conf