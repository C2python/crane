from oslo_config import cfg

debug = cfg.BoolOpt('debug',short='d',default=False,help='Turn On ddebug model')

grp = cfg.OptGroup(name='API',title='API OPTS')

api_opts = [
    cfg.IntOpt('bind_port',
                default=8000,
                help='Port Number to Listen.'),
    cfg.HostAddressOpt('host',
                default='0.0.0.0',
                help='Listening IP.'),
    cfg.StrOpt('paste_config',
                default="api-paste.ini",
                help='Path to API Paste configuration.'),
    cfg.StrOpt('uwsgi_mode',
                default='http',
                help='UWSIG MODE')
]

def add_opts():
    cfg.CONF.register_opt(debug)
    cfg.CONF.register_group(grp)
    cfg.CONF.register_opts(api_opts,group=grp)

def add_cli_opts():
    cfg.CONF.register_cli_opt(debug)
    cfg.CONF.register_cli_opts(add_opts)