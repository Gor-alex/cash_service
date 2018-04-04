# coding=utf-8
# -*- coding: utf-8 -*-

import colander

#
#
# class ProblemNode(colander.MappingSchema):
#     text_data = colander.SchemaNode(typ=_Type_(u'canceladddata', u'problem'),
#                                     validator=_Valid_(u'canceladddata', u'problem'),
#                                     missing=colander.required,
#                                     description=u'Текстовое представление проблемы')
#
#     date = colander.SchemaNode(typ=_Type_(u'canceladddata', u'datedoc'),
#                                validator=_Valid_(u'canceladddata', u'datedoc'),
#                                missing=colander.required,
#                                description=u'Дата, когда возникла проблема')


# self.colander_types = {
#     (sqlalchemy.sql.sqltypes.Integer,): colander.Integer,
#     (sqlalchemy.sql.sqltypes.SmallInteger,): colander.Integer,
#     (sqlalchemy.sql.sqltypes.BigInteger,): colander.Integer,
#     (sqlalchemy.sql.sqltypes.Float,): colander.Float,
#     (sqlalchemy.sql.sqltypes.String,): colander.String,
#     (sqlalchemy.sql.sqltypes.TIMESTAMP,): Timestamp,
#     (sqlalchemy.sql.sqltypes.Date,): Timestamp,
#     (sqlalchemy.sql.sqltypes.Time,): Timestamp,
#     (sqlalchemy.dialects.postgresql.UUID,): colander.String,
#     (sqlalchemy.dialects.postgresql.JSON,): colander.String,
#     (sqlalchemy.sql.sqltypes.DateTime,): Timestamp
# }


class SignupSchema(colander.MappingSchema):
    username = colander.SchemaNode(colander.String(), name='username')