from cornice.resource import resource, view
from cornice.validators import colander_body_validator

@resource(
    collection_path='/test', path='/test/{path}', name='Service', renderer='json'
)
class ReportPatterns(object):
    def __init__(self, request, context=None):
        self.request = request

    @view(renderer='json')
    def get(self):
        t = [u'get']
        return t

    @view(renderer='json')
    def collection_get(self):
        t = [u'collection_get']
        return t