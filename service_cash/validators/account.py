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

# {"actual_bill": 123.223, "overdraft": false, "currency": "RUB"}