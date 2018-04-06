# coding=utf-8
# -*- coding: utf-8 -*-
import decimal
from cornice.resource import resource, view
from cornice.validators import colander_body_validator
from service_cash.validators.account import Operation
from service_cash.views.account import AccountService

from service_cash import models


@resource(collection_path='/operation', path='/operation/{path}', name='Operation service')
class OperationService(object):
    def __init__(self, request, context=None):
        self.request = request

        currency = dict()
        currency[u'EUR'] = {
            u'EUR': 1,
            u'RUB': float(request.registry.settings['EUR_to_RUB']),
            u'USD': float(request.registry.settings['EUR_to_USD'])
        }
        currency[u'USD'] = {
            u'USD': 1,
            u'RUB': float(request.registry.settings['USD_to_RUB']),
            u'EUR': 1 / float(currency[u'EUR'][u'USD'])
        }

        currency[u'RUB'] = {
            u'RUB': 1,
            u'EUR': 1 / float(currency[u'EUR'][u'RUB']),
            u'USD': float(currency[u'EUR'][u'USD'])/float(currency[u'EUR'][u'RUB'])
        }
        self.currency = currency

    @view(renderer='json', accept='application/json', schema=Operation(), validators=(colander_body_validator,))
    def collection_post(self):
        # Unic identifiers
        donor = self.request.validated['donor']
        recipient = self.request.validated['recipient']
        # Answer
        success = False
        try:
            if donor != recipient:
                accounts = self.request.db.query(models.Account)\
                    .join(models.Account.currency)\
                    .filter(models.Account.idaccount.in_([donor, recipient])).all()

                db_donor, accounts = self.find_(accounts, donor)
                db_recipient, accounts = self.find_(accounts, recipient)

                if self.enough_money(db_donor) | self.overdraft(db_donor):
                    db_donor.actualbill -= decimal.Decimal(self.request.validated['delta'])
                    db_recipient.actualbill += decimal.Decimal(
                        self.request.validated['delta'] * self.currency[db_donor.currency.sname][db_recipient.currency.sname]
                    )
                    self.request.db.flush()
                    self.request.db.commit()

                    success = True

            return success

        except Exception as error:
            return AccountService.gen_error_view(error)

    def enough_money(self, db_donor):
        return self.request.validated['delta'] < float(db_donor.actualbill)

    def overdraft(self, db_donor):
        return (self.request.validated['delta'] > float(db_donor.actualbill)) & (db_donor.overdraft is True)


    @staticmethod
    def find_(objects_list, id_):
        for _db_object in objects_list:
            if _db_object.idaccount == id_:
                objects_list.remove(_db_object)
                return _db_object, objects_list

    @staticmethod
    def url_validate(request, **kwargs):
        if kwargs['request_method'] == 'GET':
            # Schema initialization
            schema = kwargs['schema']()
            # Get values
            try:
                request.validated.update(schema.deserialize(request.GET))
            except Exception as validation_error:
                request.validated['id'] = None
                request.errors.append(str(validation_error))