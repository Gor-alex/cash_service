# coding=utf-8
# -*- coding: utf-8 -*-
from sqlalchemy import create_engine, orm

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


def session_returner(request, connect_line):
    engine = create_engine(connect_line)
    Base.metadata.bind = engine
    # Configure and intense session
    session = orm.sessionmaker(bind=engine,)()

    def cleanup(request):
        if request.exception is not None:
            session.rollback()
        session.close()
    # Add cleanup after work
    request.add_finished_callback(cleanup)

    return session


def session_maker(request):
    settings = request.registry.settings
    connect_line = 'postgresql://{user}:{password}@{postgre_server}:{bd_port}/{bd_name}'.format(
        user=settings['bd_user'],
        postgre_server=settings['postgre_server'],
        bd_port=settings['bd_port'],
        password=settings['bd_password'],
        bd_name=settings['bd_name']
    )
    return session_returner(request, connect_line)