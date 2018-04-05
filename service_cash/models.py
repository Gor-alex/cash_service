# coding=utf-8
# -*- coding: utf-8 -*-

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata


class Account(Base):
    __tablename__ = 'account'

    idaccount = Column(Integer, primary_key=True, autoincrement=True)
    idcurrency = Column(ForeignKey(u'currency.idcurrency', match=u'FULL'))
    actualbill = Column(Numeric)
    overdraft = Column(Boolean)

    currency = relationship(u'Currency')


class Currency(Base):
    __tablename__ = 'currency'

    idcurrency = Column(Integer, primary_key=True)
    fname = Column(String(15))
    sname = Column(String(5))


class Operation(Base):
    __tablename__ = 'operation'

    idoperation = Column(Integer, primary_key=True)
    osumm = Column(Numeric)
    otime = Column(DateTime)


class Storage(Base):
    __tablename__ = 'storage'

    idaccount = Column(ForeignKey(u'account.idaccount', match=u'FULL'), primary_key=True, nullable=False)
    idtypeparticipant = Column(ForeignKey(u'typeparticipant.idtypeparticipant', match=u'FULL'), primary_key=True, nullable=False)
    idoperation = Column(ForeignKey(u'operation.idoperation', match=u'FULL'), primary_key=True, nullable=False)
    historybill = Column(Numeric)

    account = relationship(u'Account')
    operation = relationship(u'Operation')
    typeparticipant = relationship(u'Typeparticipant')


class Typeparticipant(Base):
    __tablename__ = 'typeparticipant'

    idtypeparticipant = Column(Integer, primary_key=True)
    sname = Column(String(15))
