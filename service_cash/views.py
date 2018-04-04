# coding=utf-8
# -*- coding: utf-8 -*-

from cornice.resource import resource, view
from cornice.validators import colander_body_validator
from service_cash.validators.post import SignupSchema
from service_cash.models import Account


@resource(
    collection_path='/test', path='/test/{path}', name='Service',
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
    # @view(renderer='json', accept='application/json', schema=SignupSchema(), validators=(colander_body_validator,))
    # def post(self):
    #     print(u'dsfadasf')

    @view(renderer='json', accept='application/json', schema=SignupSchema(), validators=(colander_body_validator,))
    def collection_post(self):
        test = self.request.db.query(Account).all()
        print(u'dsfadasf')