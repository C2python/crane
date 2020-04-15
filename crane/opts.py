from oslo_config import cfg

#grp = cfg.OptGroup(name='API',title='API OPTS')

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
                choices=['http','http-socket','socket'],
                help='UWSIG MODE')
]

_cli_options = [
    cfg.StrOpt('test',
                default="ttt",
                metavar='PATH',
                help='Path to API Paste configuration.')
]

def list_opts():
    return [
        ('DEFAULT',_cli_options),
        ('API',api_opts)
    ]