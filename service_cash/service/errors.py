# coding=utf-8
# -*- coding: utf-8 -*-
from pyramid.httpexceptions import HTTPInternalServerError


def gen_error_view(o_error):
    '''

    :param o_error: string or Exception
        String or Exception with string representation error
    :return:
        Error view
    '''
    # Create error page
    exc_view = HTTPInternalServerError()
    # Filling error field
    exc_view.explanation = o_error if isinstance(o_error, basestring) else o_error.message
    return exc_view