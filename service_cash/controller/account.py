# coding=utf-8
# -*- coding: utf-8 -*-

from service_cash.service.errors import gen_error_view
from cornice.resource import resource, view
from cornice.validators import colander_body_validator
from service_cash.validators.account import NewAccount, Url
from service_cash import models


@resource(collection_path='/account', path='/account/{path}', name='Service')
class AccountService(object):
    def __init__(self, request, context=None):
        self.request = request

    @view(renderer='json', schema=Url, validators=('url_validate',), )
    def collection_get(self):
        try:
            account = self.request.db.query(models.Account) \
                .filter(models.Account.idaccount == self.request.validated['id'])\
                .join(models.Account.currency).one()
        except Exception as error:
            return gen_error_view(error)

        return {
            u'actualbill': str(account.actualbill),
            u'currency': {
                u'sname': account.currency.sname,
                u'fname': account.currency.fname
            }
        }

    @view(renderer='json', accept='application/json', schema=NewAccount(), validators=(colander_body_validator,))
    def collection_post(self):
        try:
            currency = self.request.db.query(models.Currency.idcurrency)\
                .filter(models.Currency.sname == self.request.validated['currency']).one()

            new_account = models.Account(
                idcurrency=currency.idcurrency,
                actualbill=self.request.validated['actual_bill'],
                overdraft=self.request.validated['overdraft']
            )
            # Add new object to session
            self.request.db.add(new_account)
            # Flash it (on this bread crumb we get id account from db)
            self.request.db.flush()
            self.request.db.commit()
            return new_account.idaccount

        except Exception as error:
            return gen_error_view(error)

    @staticmethod
    def url_validate(request, **kwargs):
        """
            :param request: Request object
                Global request object
            :param kwargs: dict
                param from request
            :return: None
                Function update dict(request.validated) with valid values
        """
        if kwargs['request_method'] == 'GET':
            # Schema initialization
            schema = kwargs['schema']()
            # Get values
            try:
                request.validated.update(schema.deserialize(request.GET))
            except Exception as validation_error:
                request.validated['id'] = None
                request.errors.append(str(validation_error))
