from pyramid.config import Configurator
from pyramid.renderers import JSON


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """

    json_renderer = JSON(ensure_ascii=False)
    config = Configurator(settings=settings)
    # Add json render
    config.add_renderer('json', json_renderer)
    # Add cornice
    config.include('cornice')

    config.add_route('home', '/')
    config.scan()
    return config.make_wsgi_app()
