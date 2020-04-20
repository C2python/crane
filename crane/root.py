from pecan import expose, redirect
from webob.exc import status_map
from oslo_log import log as logging
from pecan import rest
import pecan

LOG = logging.getLogger(__name__)

class MetricController(rest.RestController):
    @pecan.expose('json')
    def get(self):
        pecan.response.status = 200
        return {'cpu':0,'mem':0}
    @pecan.expose('json')
    def post(self):
        pecan.response.status = 201
        return {'cpu':10,'mem':30}

class V1Controller(rest.RestController):
    
    def __init__(self):
        self.sub_controllers = {
            'metric': MetricController()
        }
        for name, ctrl in self.sub_controllers.items():
            setattr(self, name, ctrl)
    @pecan.expose('json')
    def index(self):
        return {
            "version": "1.0",
            "links": [
                {"rel": "self",
                 "href": pecan.request.application_url}
            ] + [
                {"rel": name,
                 "href": pecan.request.application_url + "/" + name}
                for name in sorted(self.sub_controllers)
            ]
        }