# coding=utf-8
# -*- coding: utf-8 -*-
import colander


class Transfer(colander.MappingSchema):
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
        typ=colander.Decimal(),
        validator=colander.Range(min=0),
        missing=colander.required,
        description=u'Сумма перевода'
    )