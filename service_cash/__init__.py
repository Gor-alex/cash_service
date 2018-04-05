# coding=utf-8
# -*- coding: utf-8 -*-
from pyramid.config import Configurator
from pyramid.renderers import JSON
from service_cash.service.database import session_maker


def db(request):
    '''

    :param request: Request instance
        Request
    :return:
    '''
    session = session_maker(request)
    return session

def main(global_config, **settings):
    """
        This function returns a Pyramid WSGI application.
    """

    json_renderer = JSON(ensure_ascii=False)
    config = Configurator(settings=settings)
    # Add open db session
    config.add_request_method(db, reify=True)
    # Add json render
    config.add_renderer('json', json_renderer)
    # Add cornice
    config.include('cornice')

    config.add_route('home', '/')
    config.scan()
    return config.make_wsgi_app()
