from pecan import expose, redirect
from webob.exc import status_map
from oslo_log import log as logging
from pecan import rest
import pecan

LOG = logging.getLogger(__name__)

class V1Controller(rest.RestController):

    @pecan.expose()
    def get(self):
        pecan.response.status = 200
        return "This is V1 Controller Get.\n"
    @pecan.expose()
    def post(self):
        pecan.response.status = 201
        return "This is V1 Controller Post.\n"