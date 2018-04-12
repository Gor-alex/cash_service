# coding=utf-8
# -*- coding: utf-8 -*-
import decimal
from datetime import datetime
from cornice.resource import resource, view
from cornice.validators import colander_body_validator
from service_cash.validators.operation import Transfer
from service_cash.service.errors import gen_error_view
from service_cash import models


@resource(collection_path='/transfer', path='/transfer/{path}', name='Operation service')
class OperationService(object):
    def __init__(self, request, context=None):
        self.request = request

        currency = dict()
        currency[u'EUR'] = {
            u'EUR': 1,
            u'RUB': decimal.Decimal(request.registry.settings['EUR_to_RUB']),
            u'USD': decimal.Decimal(request.registry.settings['EUR_to_USD'])
        }
        currency[u'USD'] = {
            u'USD': 1,
            u'RUB': decimal.Decimal(request.registry.settings['USD_to_RUB']),
            u'EUR': 1 / decimal.Decimal(currency[u'EUR'][u'USD'])
        }

        currency[u'RUB'] = {
            u'RUB': 1,
            u'EUR': 1 / decimal.Decimal(currency[u'EUR'][u'RUB']),
            u'USD': decimal.Decimal(currency[u'EUR'][u'USD'])/decimal.Decimal(currency[u'EUR'][u'RUB'])
        }
        self.currency = currency

    @view(renderer='json', accept='application/json', schema=Transfer(), validators=(colander_body_validator,))
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
                if len(accounts) != 2:
                    return gen_error_view('Для совершения операции перевода, необходимо два разных счёта')

                db_donor, accounts = self.find_(accounts, donor)
                db_recipient, accounts = self.find_(accounts, recipient)

                if self.enough_money(db_donor) | self.overdraft(db_donor):
                    # Creating operation
                    operation = models.Operation(
                        otime=datetime.now(),
                        osumm=self.request.validated['delta']
                    )
                    # adding operation to db snapshot
                    self.request.db.add(operation)
                    # Get operation.idoperation from autoincrement function
                    self.request.db.flush()

                    # Add operation to history
                    self.request.db.add_all(
                        [
                            models.Storage(
                                idaccount=db_donor.idaccount,
                                idtypeparticipant=1,
                                idoperation=operation.idoperation,
                                historybill=db_donor.actualbill
                            ),
                            models.Storage(
                                idaccount=db_recipient.idaccount,
                                idtypeparticipant=2,
                                idoperation=operation.idoperation,
                                historybill=db_recipient.actualbill
                            )
                        ]
                    )

                    # Money transfer
                    db_donor.actualbill -= decimal.Decimal(self.request.validated['delta'])
                    db_recipient.actualbill += decimal.Decimal(
                        self.request.validated['delta'] * self.currency[db_donor.currency.sname][db_recipient.currency.sname]
                    )
                    self.request.db.flush()

                    # Commit changes to db
                    self.request.db.commit()
                    # Change status operation on success
                    success = True

            return success

        except Exception as error:
            return gen_error_view(error.message)

    def enough_money(self, db_donor):
        return self.request.validated['delta'] < db_donor.actualbill

    def overdraft(self, db_donor):
        return (self.request.validated['delta'] > db_donor.actualbill) & (db_donor.overdraft is True)

    @staticmethod
    def find_(objects_list, id_):
        """

        :param objects_list: list
            list of db objects
        :param id_: int
            wanted id account
        :return: model.Account, [model.Account...]
            Account object

        """
        for _db_object in objects_list:
            if _db_object.idaccount == id_:
                objects_list.remove(_db_object)
                return _db_object, objects_list
