# coding=utf-8
# -*- coding: utf-8 -*-

import colander


class Url(colander.MappingSchema):
    id_account = colander.SchemaNode(
        name='id',
        typ=colander.Int(),
        missing=colander.required,
        description=u'Уникальный индентификатор интересующего нас аккайнта'
    )

class NewAccount(colander.MappingSchema):
    actual_bill = colander.SchemaNode(
        name='actual_bill',
        typ=colander.Float(),
        validator=colander.Range(min=0),
        missing=colander.required,
        description=u'Актуальная сумма на счёте (В момент открытия)'
    )
    overdraft = colander.SchemaNode(
        name='overdraft',
        typ=colander.Bool(),
        missing=colander.required,
        description=u'Возможность овердрафта (True/False)'
        )
    currency = colander.SchemaNode(
        name='currency',
        typ=colander.String(),
        validator=colander.OneOf(['USD', 'RUB', 'EUR']),
        missing=colander.required,
        description=u'Базовая валюта для банковского счёта'
    )


# идентификатор счета донора, идентификатор счета реципиента, сумма перевода(валюта определяется по счетам)
class Operation(colander.MappingSchema):
    donor = colander.SchemaNode(
        name='donor',
        typ=colander.Int(),
        validator=colander.Range(min=0),
        missing=colander.required,
        description=u'Id account - уникальный индификатор донора'
    )

    recipient = colander.SchemaNode(
        name='recipient',
        typ=colander.Int(),
        validator=colander.Range(min=0),
        missing=colander.required,
        description=u'Id account - уникальный индификатор получателя'
    )
    delta = colander.SchemaNode(
        name='delta',
        typ=colander.Float(),
        validator=colander.Range(min=0),
        missing=colander.required,
        description=u'Сумма перевода'
    )


# {"actual_bill": 123.223, "overdraft": false, "currency": "RUB"}
# {"donor": 2, "recipient": 3, "delta": 1}