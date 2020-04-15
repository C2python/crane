from oslo_log import log
from crane import opts
from oslo_config import cfg

def prepare_service(conf=None,args=None,config_file=None):
    if conf is None:
        conf = cfg.ConfigOpts()
    for group,options in opts.list_opts():
        conf.register_opts(list(options),
                            group=None if group == 'DEFAULT' else group)
    conf.register_cli_opts(opts._cli_options)
    log.register_options(conf)
    log.setup(conf,'crane')
    return conf